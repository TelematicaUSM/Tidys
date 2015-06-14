# -*- coding: UTF-8 -*-

from unicodedata import normalize
from tornado.gen import coroutine
from pymongo import ASCENDING
from .common import db
from .db_object import DBObject

class Course(DBObject):
    coll = db.courses
    path = 'src.db.course.Course'

    @classmethod
    @coroutine
    def create(cls, user, name):
        compacted_name = name.replace(' ', '')
        norm_name = normalize('NFKC', compacted_name)
        casefolded_name = norm_name.casefold()
        _id = str(user.id) + casefolded_name

        self = yield super().create(_id)
        yield self.store_dict(
            {'name': name, 'user_id': user.id})
        return self

    @classmethod
    @coroutine
    def get_user_courses(cls, user):
        yield cls.coll.ensure_index(
            [('user_id', ASCENDING),
             ('_id', ASCENDING)])

        cursor = cls.coll.find({'user_id': user.id},
                               {'name': True},
                               sort=[('_id', ASCENDING)])

        courses = yield cursor.to_list(None)
        return courses

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{0.__class__.__name__}('{0.id}')".format(
            self)

    @property
    def name(self):
        return self._data['name']
