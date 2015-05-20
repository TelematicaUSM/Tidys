# -*- coding: UTF-8 -*-

"""MongoDB PUB-SUB message broker

This module provides the functions necesary to send and
subscribe other functions to a PUB-SUB messaging system.
The messaging system is implemented using MongoDB's tailable
cursors and capped collections.
"""

from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Task
from pymongo.errors import CollectionInvalid

from src import messages as msg
from .common import db
from .db_object import DBObject


_path = 'src.db.message_broker'

_coll_name = 'messages'
_coll = db[_coll_name]
_actions = {}
_owners = {}
cursor = None


def register_action(owner, msg_type, action):
    if owner in _owners:
        _owners[owner].add((msg_type, action))
    else:
        _owners[owner] = {(msg_type, action)}

    if msg_type in _actions:
        _actions[msg_type].add(action)
    else:
        _actions[msg_type] = {action}


def remove_owner(owner):
    for msg_type, action in _owners[owner]:
        _actions[msg_type].discard(action)

        if not _actions[msg_type]:
            del _actions[msg_type]

    del _owners[owner]


def on_message(message):
    code_path = _path + '.on_message'

    try:
        for action in _actions[message['type']]:
            IOLoop.current().spawn_callback(action, message)

    except KeyError:
        if 'type' in message:
            msg.unrecognized_db_message_type(code_path,
                                             message)
        else:
            msg.malformed_db_message(code_path, message)


@coroutine
def send_message(message):
    if not isinstance(message, dict): raise TypeError
    if 'type' not in message: raise ValueError
    yield _coll.insert(message)


@coroutine
def _tailable_iteration(function: 'callable' = None,
                        stop: bool = True,
                        sleep: int = 0):
    global cursor

    while True:
        if not cursor or not cursor.alive:
            cursor = _coll.find(tailable=True,
                                await_data=True)

        if (yield cursor.fetch_next):
            message = cursor.next_object()
            if function: function(message)
        elif stop: return

        if sleep: yield Task(IOLoop.current().call_later,
                             sleep)


@coroutine
def _broker_loop():
    try:
        yield db.create_collection(_coll_name, capped=True,
                                   size=1000000)
    except CollectionInvalid:
        pass

    yield _tailable_iteration()
    yield _tailable_iteration(function=on_message,
                              stop=False, sleep=1)


#This starts the loop the first time this module is imported
IOLoop.current().spawn_callback(_broker_loop)
