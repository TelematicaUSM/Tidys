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

from src.pub_sub import OwnerPubSub
from .common import db


_path = 'src.db.message_broker'

_coll_name = 'messages'
_coll = db[_coll_name]
cursor = None
_ps = OwnerPubSub()

# METHOD ALIASES:
register = _ps.register
remove_owner = _ps.remove_owner


@coroutine
def send_message(message):
    if not isinstance(message, dict):
        raise TypeError

    if 'type' not in message:
        raise ValueError

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
            if function:
                function(message)
        elif stop:
            return

        elif sleep:
            yield Task(IOLoop.current().call_later, sleep)


@coroutine
def _broker_loop():
    try:
        yield db.create_collection(_coll_name, capped=True,
                                   size=1000000)
    except CollectionInvalid:
        pass

    yield _tailable_iteration()
    yield _tailable_iteration(
        function=_ps.distribute_message, stop=False,
        sleep=1)


# This starts the loop the first time this module is
# imported
IOLoop.current().spawn_callback(_broker_loop)
