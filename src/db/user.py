# -*- coding: UTF-8 -*-

from tornado.gen import coroutine
from src import messages
from src.utils import random_word
from .common import db
from .db_object import DBObject

class User(DBObject):
    coll = db.users
    
    @classmethod
    @coroutine
    def from_google_userinfo(cls, userinfo):
        """Creates a User object from google's userinfo.
           Sample userinfo data:
            {'family_name': 'Ganter',
             'given_name': 'Cristóbal',
             'kind': 'plus#personOpenIdConnect',
             'locale': 'es',
             'name': 'Cristóbal Ganter',
             'picture': 'https://lh4.googleusercontent.com/
                         -draGfxB6y6U/AAAAAAAAAAI/
                         AAAAAAAAC3I/-N8omtu2PN4/photo.jpg?
                         sz=50',
             'profile': 'https://plus.google.com/
                         117984339433749478236',
             'sub': '117984339433749478236'}"""
             
        try:
            yield cls.coll.update(
                {'_id': userinfo['sub']},
                {
                    '$set': {'google_userinfo': userinfo}
                },
                upsert = True)
            self = yield cls(userinfo['sub'])
            return self
        
        except:
            messages.unexpected_error(
                'src.db.user.User.from_google_userinfo')
            raise
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "User('%s')" % self.id

    @property
    def secret(self):
        if 'secret' in self._data:
            return self._data['secret']
        else:
            secret = random_word(20)
            self.store('secret', secret)
            return secret
    
    @property
    def name(self):
        return self.google_userinfo['name']
