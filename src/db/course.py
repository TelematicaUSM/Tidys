# -*- coding: UTF-8 -*-

from unicodedata import normalize

from tornado.gen import coroutine
from pymongo import ASCENDING

from src.exceptions import NotDictError
from .common import db
from .db_object import DBObject


class Course(DBObject):
    coll = db.courses
    path = 'src.db.course.Course'

    @property
    def name(self):
        return self._data['name']

    def __str__(self):
        return self.name

    @classmethod
    @coroutine
    def create(cls, user, name):
        compacted_name = name.replace(' ', '')
        norm_name = normalize('NFKC', compacted_name)
        casefolded_name = norm_name.casefold()
        id_ = str(user.id) + casefolded_name

        self = yield super().create(id_)
        yield self.store_dict(
            {'name': name, 'user_id': user.id})
        return self

    @classmethod
    @coroutine
    def _get_courses(cls, spec, fields=None):
        """Return a list of courses.

        Returns a list of courses that meet the restrictions
        set by the ``spec`` parameter.

        :param dict spec:
            This parameter is passed directly to the
            ``MotorCollection.find`` method. The dictionary
            can contain any valid MongoDB query operator.

        :param fields:
            This parameter is passed directly to the
            ``MotorCollection.find`` method.

        :type fields: dict or list

        :return:
            A future that resolves to a list.

        :raises src.exceptions.NotDictError:
            If ``spec`` is not a dictionary.
        """
        try:
            cursor = cls.coll.find(
                spec, fields, sort=[('_id', ASCENDING)])

            courses = yield cursor.to_list(None)
            return courses

        except TypeError as te:
            if not isinstance(spec, dict):
                raise NotDictError('spec') from te

            if not isinstance(fields, (dict, list)) and \
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
    def get_user_courses(cls, user):
        """Get all curses created by ``user``.

        :param User user:
            The user who created the courses to be obtained.

        :return:
            A future that resolves to a list of couses.
        """
        try:
            yield cls.coll.ensure_index(
                [('user_id', ASCENDING), ('_id', ASCENDING)]
            )

            courses = yield cls._get_courses(
                spec={'user_id': user.id}, fields=['name'])
            return courses

        except:
            raise

    @classmethod
    @coroutine
    def get_courses_from_ids(cls, ids):
        """Get all courses specified by the ids parameter.

        :param list ids:
            A list of the IDs of the documents to be
            fetched.

        :return:
            A future that resolves to a list of courses.
        """
        try:
            courses = yield cls._get_courses(
                {
                    '_id': {'$in': ids}
                }
            )
            return courses

        except:
            raise

    @coroutine
    def count_students(self):
        """Count the number of students in this course.

        :return:
            The number of students currently participating
            in this course.
        :rtype:
            A future that resolves to ``int``.

        :raises OperationFailure:
            On a database error.
        """
        try:
            yield db.users.ensure_index(
                [
                    ('course_id', ASCENDING),
                    ('status', ASCENDING)
                ],
                sparse=True
            )

            cursor = db.users.find(
                {'course_id': self.id, 'status': 'seat'})
            count = yield cursor.count()
            return count

        except:
            raise
