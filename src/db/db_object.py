from tornado.gen import coroutine
from bson.dbref import DBRef
from pymongo.errors import DuplicateKeyError, \
                           OperationFailure
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
            self.store(name, value)
    
    def setattr(self, name, value):
        super().__setattr__(name, value)
    
    @coroutine
    def store(self, name, value):
        self._data[name] = value
        yield self.coll.update(
            {'_id': self.id},
            {
                '$set':{name: value}
            }
        )
    
    @coroutine
    def store_dict(self, d):
        yield self.coll.update(
            {'_id': self.id},
            {
                '$set': d
            }
        )
        self._data.update(d)
    
    @property
    def id(self):
        return self._data['_id']
    
#    @classmethod
#    @coroutine
#    def get_or_create(cls, _id):
#        """Returns an object from the database, if it
#        doesn't exist, it creates it."""
#        try:
#            code_path = cls.path + '.get_or_create'
#            
#            try:
#                self = yield cls(_id)
#                
#            except NoObjectReturnedFromDB:
#                self = yield cls.create(_id)
#                
#            return self
#            
#        except DuplicateKeyError:
#            msg.impossible_condition(code_path)
#        
#        except:
#            msg.unexpected_error(code_path)
#            raise
