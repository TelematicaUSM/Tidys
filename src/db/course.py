# -*- coding: UTF-8 -*-

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
        self = yield super().create(
            {'name': name, 'user_id': user.id})
        return self
    
    @classmethod
    @coroutine
    def get_user_course_names(cls, user):
        yield cls.coll.ensure_index('_id.user_id')
        
        cursor = cls.coll.find(
            filter={'_id.user_id': user.id},
            projection={'_id.name': 1},
            sort=[('_id', ASCENDING)])
            
        courses = yield cursor.to_list(None)
        
        return [c['_id']['name'] for c in courses]
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "{0.__class__.__name__}('{0.id}')".format(
            self)
    
    @property
    def name(self):
        return self.id['name']
