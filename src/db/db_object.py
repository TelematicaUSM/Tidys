# -*- coding: UTF-8 -*-

from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from bson.dbref import DBRef
from pymongo.errors import DuplicateKeyError
from src import messages as msg
from .common import NoObjectReturnedFromDB

class DBObject(object):
    path = 'src.db.db_object.DBObject'
    
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
            raise NoObjectReturnedFromDB
        
        self = super().__new__(cls)
        self.setattr('_data', data)
        return self
    
    @classmethod
    @coroutine
    def create(cls, _id, **kwargs):
        """Creates a new object in the database and returns
        the created object."""
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
        else:
            raise AttributeError
    
    def __setattr__(self, name, value):
        if hasattr(self, name):
            self.setattr(name, value)
        else:
            IOLoop.current().spawn_callback(
                self.store, name, value, update_data=False)
            self._data[name] = value
    
    def setattr(self, name, value):
        super().__setattr__(name, value)
    
    @coroutine
    def store(self, name, value, update_data):
        yield self.store_dict({name: value}, update_data)
    
    @coroutine
    def store_dict(self, d, update_data=True):
        yield self.coll.update({'_id': self.id},
                               {'$set': d})
        if update_data:
            self._data.update(d)
    
    @property
    def id(self):
        return self._data['_id']
