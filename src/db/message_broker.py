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


@coroutine
def _send_message(message):
    yield _coll.insert(message)

_ps = OwnerPubSub(
    name='db_pub_sub',
    send_function=_send_message
)

# METHOD ALIASES:
register = _ps.register
send_message = _ps.send_message
remove_owner = _ps.remove_owner


@coroutine
def _tailable_iteration(function: 'callable'=None,
                        stop: bool=True,
                        sleep: int=0):
    """Iterates through a tailable cursor.

    .. todo::
        *   Use ``tornado.gen.sleep`` instead of
            ``Task(IOLoop.current().call_later, sleep)``.
    """
    global cursor

    while True:
        if cursor is None or not cursor.alive:
            cursor = _coll.find(tailable=True,
                                await_data=True)

        if (yield cursor.fetch_next):
            message = cursor.next_object()
            if function is not None:
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
        function=_ps.execute_actions, stop=False,
        sleep=1)


# This starts the loop the first time this module is
# imported
IOLoop.current().spawn_callback(_broker_loop)
