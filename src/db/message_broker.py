# -*- coding: UTF-8 -*-

from tornado.gen import coroutine
from src import messages as msg
from .common import db
from .db_object import DBObject

coll = db.messages
path = 'src.db.message_broker'
actions = {}

def register_action(msg_type, action):
    if msg_type in actions:
        actions[msg_type].add(action)
    else:
        actions[msg_type] = {action}

def on_message(self, message):
    code_path = path + '.on_message'
    
    try:
        for action in actions[message['type']]:
            action(message)
    
    except KeyError:
        if 'type' in message:
            msg.unrecognized_db_message_type(code_path,
                                             message)
        else:
            msg.malformed_db_message(code_path, message)

def _
    
#    @classmethod
#    @coroutine
#    def create(cls, user, name):
#        compacted_name = name.replace(' ', '')
#        norm_name = normalize('NFKC', compacted_name)
#        casefolded_name = norm_name.casefold()
#        _id = str(user.id) + casefolded_name
#        
#        self = yield super().create(_id)
#        self.store_dict({'name': name, 'user_id': user.id})
#        return self
#    
#    @classmethod
#    @coroutine
#    def get_user_courses(cls, user):
#        yield cls.coll.ensure_index(
#            [('user_id', ASCENDING),
#             ('_id', ASCENDING)])
#        
#        cursor = cls.coll.find({'user_id': user.id},
#                               {'name': True},
#                               sort=[('_id', ASCENDING)])
#            
#        courses = yield cursor.to_list(None)
#        return courses
#    
#    def __str__(self):
#        return self.name
#    
#    def __repr__(self):
#        return "{0.__class__.__name__}('{0.id}')".format(
#            self)
#    
#    @property
#    def name(self):
#        return self.id['name']
