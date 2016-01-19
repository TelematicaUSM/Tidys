# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from pymongo import ASCENDING
from bson.dbref import DBRef

from src.exceptions import NotDictError
from .common import ConditionNotMetError, \
    NoObjectReturnedFromDB, db


class DBObject(object):

    r"""Interface object to communicate to the database.

    This object should not be instanced directly. Instead,
    you must inherit from DBObject and define the ``coll``
    attribute in the new class.

    .. todo::
        * review error handling
        * use is not none instead of not data
        * remove ``*_if`` methods and add a
          ``condition`` optional parameter in the original
          functions
    """

    defaults = {}

    @classmethod
    def _check_get_arguments(cls, id_, dbref):
        if id_ is not None and dbref is not None:
            raise ValueError(
                'Only one reference argument should be '
                'specified.')

        if dbref is not None and \
                dbref.collection != cls.coll:
            raise ValueError(
                "dbref doesn't match this class's "
                "collection")

    @classmethod
    @coroutine
    def get(cls, id_=None, dbref=None, **kwargs):
        """Get an instance from a document.

        This method gets a document from the database and
        wraps it in an instance of this class. One and only
        one of the parameters ``id_`` and ``dbref`` should
        be specified.

        :param str id_:
            Identifier of the document that will be fetched
            from the database.

        :param DBRef dbref:
            DBRef object used to find the document in the
            database.

        :return:
            An instance of this class that represents a
            document of the database.

        :raises ValueError:
            If none or both of the arguments are
            specified or if the collection in ``dbref`` does
            not match this class's collection.

        :raises TypeError:
            If ``dbref`` is not an instance of ``DBRef``.

        :raises AttributeError:
            If ``dbref`` doesn't have the ``collection``
            attribute.
        """
        try:
            cls._check_get_arguments(id_, dbref)

            if id_:
                data = yield cls.coll.find_one({'_id': id_})
            elif dbref:
                data = yield db.dereference(dbref)
            else:
                raise ValueError(
                    'Either id_ or dbref should be '
                    'specified.')

            if data is None:
                raise NoObjectReturnedFromDB(cls)

            return cls(data, **kwargs)

        except AttributeError as ae:
            if not hasattr(dbref, 'collection'):
                e = AttributeError(
                    "dbref doesn't have the collection "
                    "attribute. Maybe dbref is not an "
                    "instance of DBRef.")
                raise e from ae
            else:
                raise

        except TypeError as te:
            if not isinstance(dbref, DBRef):
                e = TypeError(
                    'dbref has to be an instance of DBRef.')
                raise e from te
            else:
                raise

    @classmethod
    @coroutine
    def create(cls, id_, **kwargs):
        """Create a new object in the database.

        :param str id_:
            Identifier of the document that will be fetched
            from the database.

        :param kwargs:
            Keyword arguments to be passed to the class
            constructor.

        :return:
            An instance of this class that represents the
            newly created document.

        :raises pymongo.errors.OperationFailure:
            If an error occurred during insertion.

        :raises pymongo.errors.DuplicateKeyError:
            If an object with the same id alredy exists in
            the database.
            :class:`~pymongo.errors.DuplicateKeyError` is a
            subclass of
            :class:`~pymongo.errors.OperationFailure`.
        """
        try:
            yield cls.coll.insert({'_id': id_})
            self = yield cls.get(id_, **kwargs)
            return self

        except:
            raise

    @classmethod
    @coroutine
    def get_list(cls, spec, fields=None):
        """Return a list of documents.

        Returns a list of documents that meet the
        restrictions set by the ``spec`` parameter.

        :param dict spec:
            This parameter is passed directly to the
            :meth:`motor.MotorCollection.find` method. The
            dictionary can contain any valid MongoDB query
            operator.

        :param fields:
            This parameter is passed directly to the
            :meth:`motor.MotorCollection.find` method.

        :type fields: dict or list

        :return:
            A future that resolves to a list of documents.

        :raises src.exceptions.NotDictError:
            If ``spec`` is not a dictionary.
        """
        try:
            cursor = cls.coll.find(
                spec, fields, sort=[('_id', ASCENDING)])

            documents = yield cursor.to_list(None)
            return documents

        except TypeError as te:
            if not isinstance(spec, dict):
                raise NotDictError('spec') from te

            elif not isinstance(fields, (dict, list)) and \
                    fields is not None:
                e = TypeError(
                    'The fields parameter should be a '
                    'dictionary or a list.'
                )
                raise e from te

            else:
                raise

    @classmethod
    @coroutine
    def get_one_document(cls, id_, fields=None):
        """Get a raw document from the database.

        :param id_:
            The ID of the object to be fetched from the
            database.

        :param fields:
            The fields to be included in the document.
        :type fields: list of names or dict ({names: bool})

        :return:
            The specified document.
        :rtype: dict

        :raises NoObjectReturnedFromDB:
            If there is no document with the specified ID in
            the database.
        """
        try:
            document = yield cls.coll.find_one(
                id_, fields=fields)

            if document is None:
                raise NoObjectReturnedFromDB(cls)

            else:
                return document
        except:
            raise

    def __init__(self, data, **kwargs):
        if isinstance(data, dict):
            self.setattr('_data', data)
        else:
            raise NotDictError(
                'data',
                'Found {}.'.format(
                    type(data)
                )
            )

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

    def __str__(self):
        return self.id

    def __repr__(self):
        return "{classname}.get('{id}')".format(
            classname=self.__class__.__name__, id=self.id)

    @property
    def id(self):
        return self._data['_id']

    def setattr(self, name, value):
        super().__setattr__(name, value)

    @coroutine
    def store(self, name, value, update_data=True):
        """Store a value in a field of this document.

        :param str name:
            The name of the field to be stored.

        :param object value:
            The value that will be stored in the field.

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
        """
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
        """Modify the document associated with this object.

        :param dict effect:
            Changes to be made to the document. This is
            equivalent to ``collection.update()``s
            ``update`` parameter.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.

        :raises NotDictError:
            If ``effect`` is not a dictionary.
        """
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
            equivalent to ``collection.update()``s
            ``update`` parameter.

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

        :param list \*fields:
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

        :param list \*fields:
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
        try:
            data = yield self.coll.find_one(
                {'_id': self.id},
                fields if fields else None
            )

            if not data:
                raise NoObjectReturnedFromDB(self.__class__)

            if fields:
                self._data.update(data)
            else:
                self.setattr('_data', data)
        except:
            raise
