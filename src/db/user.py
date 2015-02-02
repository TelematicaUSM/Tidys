# -*- coding: UTF-8 -*-

import jwt

from tornado.gen import coroutine
from src.utils import random_word
from .common import db
from .db_object import DBObject

class User(DBObject):
    coll = db.users
    
    @classmethod
    @coroutine
    def from_google_data(cls, g_data):
        _id = jwt.decode(g_data['id_token'],
                         verify=False)['id']
        yield cls.coll.update(
            {'_id': _id},
            {
                '$set': {'google_data': g_data}
            },
            upsert = True
        )
        self = yield cls(_id)
        return self
    
    @property
    def secret(self):
        if 'secret' in self._data:
            return self._data['secret']
        else:
            secret = random_word(20)
            self.store('secret', secret)
            return secret
