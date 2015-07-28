# -*- coding: UTF-8 -*-

from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from pymongo.errors import DuplicateKeyError
from bson.dbref import DBRef

from src import messages as msg
from src.exeptions import NotDictError
from .common import ConditionNotMetError, \
    NoObjectReturnedFromDB, db


class DBObject(object):

    r"""Interface object to communicate to the database.

    This object should not be instanced directly. Instead,
    you must inherit from DBObject and define the ``coll``
    attribute in the new class.

    .. todo::
        * create a constructor instead of overriding
          __new__.
        * change \_id with id\_
        * review error handling
        * use is not none instead of not data
    """

    defaults = {}
    path = 'src.db.db_object.DBObject'

    @property
    def id(self):
        return self._data['_id']

    @coroutine
    def __new__(cls, _id=None, dbref=None):
        if bool(_id) == bool(dbref):
            raise ValueError

        if _id:
            data = yield cls.coll.find_one({'_id': _id})
        elif not isinstance(dbref, DBRef):
            raise TypeError
        elif dbref.collection != cls.coll:
            raise ValueError
        else:
            data = yield db.dereference(dbref)

        if not data:
            raise NoObjectReturnedFromDB(cls)

        self = super().__new__(cls)
        self.setattr('_data', data)
        return self

    @classmethod
    @coroutine
    def create(cls, _id, **kwargs):
        """Create a new object in the database.

        :return: The created object.
        """
        try:
            yield cls.coll.insert({'_id': _id})
            self = yield cls(_id, **kwargs)
            return self

        except DuplicateKeyError:
            msg.duplicate_object_in_db(cls.path + '.create',
                                       _id)
            raise

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]

        elif name in self.defaults:
            return self.defaults[name]

        else:
            raise AttributeError

    def __setattr__(self, name, value):
        """Set an attribute using the dot notation.

        .. note:: this is dangerous!
        """
        if hasattr(self, name):
            self.setattr(name, value)
        else:
            IOLoop.current().spawn_callback(
                self.store, name, value, update_data=False)
            self._data[name] = value

    def setattr(self, name, value):
        super().__setattr__(name, value)

    @coroutine
    def store(self, name, value, update_data=True):
        yield self.store_dict({name: value}, update_data)

    @coroutine
    def store_dict(self, d, update_data=True):
        """Store a dictionary in this document.

        :param dict d:
            A dictionary containing the attributes that will
            be stored in the corresponding document of the
            database.

        :param bool update_data:
            If true, ``self._data`` will be updated locally
            without reading from the database. If False,
            ``self._data`` will not be updated even after
            successfully writing to the database. This is
            useful (but dangerous) when you want to call
            this method using
            ``IOLoop.current().spawn_callback()`` and you
            update the local copy (``self._data``) manually.
            This can happen when you have to call this
            method, from a method that is not a coroutine.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.

        :raises NotDictError:
            If ``condition`` or ``d`` are not a dictionary.
        """
        yield self.store_dict_if({}, d, update_data)

    @coroutine
    def store_dict_if(self, condition, d, update_data=True):
        """Store a dictionary in this document.

        This function uses the ``collection.update()``
        method. The result of ``collection.update()`` isn't
        documented in pymongo 2.8. I found it was of the
        form::

            {'n': 1,
             'nModified': 1,
             'ok': 1,
             'updatedExisting': True}

        Where I assume ``n`` is equivalent to ``nMatched``,
        ``nModified`` is described in MongoDB's
        documentation, I have no idea what ``ok`` is and
        ``updatedExisting`` is there for backwards
        compatibility.

        :param dict condition:
            Condition that has to be met to update this
            document. Here you can use all the MongoDB's
            query selectors.

        :param dict d:
            A dictionary containing the attributes that will
            be stored in the corresponding document of the
            database.

        :param bool update_data:
            If true, ``self._data`` will be updated locally
            without reading from the database. If False,
            ``self._data`` will not be updated even after
            successfully writing to the database. This is
            useful (but dangerous) when you want to call
            this method using
            ``IOLoop.current().spawn_callback()`` and you
            update the local copy (``self._data``) manually.
            This can happen when you have to call this
            method, from a method that is not a coroutine.

        :raises ConditionNotMetError:
            If the document associated with this object does
            not meet the condition specified by
            ``condition`` or if the document no longer
            exists in the database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.

        :raises NotDictError:
            If ``condition`` or ``d`` are not a dictionary.

        .. todo::
            *   Use Exception instead of assert.

        .. note::
            You can implement an equivalent operation using
            the :meth:`DBObject.modify_if` method. The
            difference between this two methods is that
            :meth:`DBObject.store_dict_if` updates only the
            specified attributes in the local object.
            Whereas :meth:`DBObject.modify_if` updates the
            whole data of the local object. You should take
            this in consideration if your documents are big
            or if you perform a huge number of operations.
            In those cases it is more efficient to use
            :meth:`DBObject.store_dict_if`.
        """
        try:
            condition.update(_id=self.id)
            result = yield self.coll.update(condition,
                                            {'$set': d})
            assert result['n'] in (0, 1)

            if result['n'] == 0:
                raise ConditionNotMetError(details=result)

            if update_data:
                self._data.update(d)

        except (TypeError, AttributeError) as e:
            if not isinstance(condition, dict):
                raise NotDictError('condition') from e

            elif not isinstance(d, dict):
                raise NotDictError('d') from e

            else:
                raise

    @coroutine
    def modify(self, effect):
        yield self.modify_if({}, effect)

    @coroutine
    def modify_if(self, condition, effect):
        """Modify this document if a condition is met.

        Modifies the document associated with this object if
        ``condition`` is met. This is useful to make atomic
        operations in the document, changing the document
        only if your assumptions are still valid in the
        representation of the object that is in the
        database.

        :param dict condition:
            Condition that has to be met to update this
            document. Here you can use all the MongoDB's
            query selectors.

        :param dict effect:
            Changes to be made to the document. This is
            equivalent to "collection.update()" "update"
            parameter.

        :raises ConditionNotMetError:
            If the document associated with this object does
            not meet the condition specified by
            ``condition`` or if the document no longer
            exists in the database.

        :raises NotDictError:
            If ``condition`` or ``effect`` are not a
            dictionary.
        """
        try:
            condition.update(_id=self.id)

            data = yield self.coll.find_and_modify(
                condition, effect, new=True)

            if data is None:
                raise ConditionNotMetError()
            else:
                self.setattr('_data', data)

        except (TypeError, AttributeError) as e:
            if not isinstance(condition, dict):
                raise NotDictError('condition') from e

            elif not isinstance(effect, dict):
                raise NotDictError('effect') from e

            else:
                raise

    @coroutine
    def reset(self, *fields, update_data=True):
        """Reset some fields to their default values.

        :param list *fields:
            A list of strings, containing the names of the
            attributes to be changed to their default
            values.

        :param bool update_data:
            If true, ``self._data`` will be updated locally
            without reading from the database. If False,
            ``self._data`` will not be updated even after
            successfully writing to the database. This is
            useful (but dangerous) when you want to call
            this method using
            ``IOLoop.current().spawn_callback()`` and you
            update the local copy (``self._data``) manually.
            This can happen when you have to call this
            method, from a method that is not a coroutine.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.

        :raises KeyError:
            If one of the fields is not in
            ``self.defaults``.
        """
        yield self.reset_if(
            {}, *fields, update_data=update_data)

    @coroutine
    def reset_if(
            self, condition, *fields, update_data=True):
        """Reset some fields to their default values.

        :param dict condition:
            Condition that has to be met to update this
            document. Here you can use all the MongoDB's
            query selectors.

        :param list *fields:
            A list of strings, containing the names of the
            attributes to be changed to their default
            values.

        :param bool update_data:
            If true, ``self._data`` will be updated locally
            without reading from the database. If False,
            ``self._data`` will not be updated even after
            successfully writing to the database. This is
            useful (but dangerous) when you want to call
            this method using
            ``IOLoop.current().spawn_callback()`` and you
            update the local copy (``self._data``) manually.
            This can happen when you have to call this
            method, from a method that is not a coroutine.

        :raises ConditionNotMetError:
            If the document associated with this object does
            not meet the condition specified by
            ``condition`` or if the document no longer
            exists in the database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.

        :raises NotDictError:
            If ``condition`` is not a dictionary.

        :raises KeyError:
            If one of the fields is not in
            ``self.defaults``.
        """
        try:
            yield self.store_dict_if(
                condition,
                {f: self.defaults[f] for f in fields},
                update_data
            )
        except KeyError as ke:
            if not all(f in self.defaults for f in fields):
                e = KeyError(
                    'One of the attributes is not in the '
                    'defaults dictionary.')
                raise e from ke
            else:
                raise

    @coroutine
    def sync(self, *fields):
        data = yield self.coll.find_one(
            {'_id': self.id}, fields if fields else None)

        if not data:
            raise NoObjectReturnedFromDB(self.__class__)

        self.setattr('_data', data)
