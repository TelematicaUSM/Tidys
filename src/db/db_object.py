from sys import exc_info
from logging import error
from tornado.gen import coroutine
from .common import NoObjectReturnedFromDB

class DBObject(object):
    @coroutine
    def __new__(cls, _id):
        try:
            data = yield cls.coll.find_one({'_id': _id})
            if not data:
                raise NoObjectReturnedFromDB

            self = super().__new__(cls)
            self.setattr('_data', data)
            return self
        
        except NoObjectReturnedFromDB:
            raise
            
        except:
            error('src.db.DBObject.__new__: '
                  'Unexpected error: %s', exc_info()[0])
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
            self.store(name, value)
    
    def setattr(self, name, value):
        super().__setattr__(name, value)
    
    def store(self, name, value):
        self._data[name] = value
        self.coll.update(
            {'_id': self.id},
            {
                '$set':{name: value}
            }
        )
    
    @property
    def id(self):
        return self._data['_id']
