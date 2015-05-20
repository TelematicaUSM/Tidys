# -*- coding: UTF-8 -*-

from tornado.gen import coroutine
from motor import MotorClient
from conf import database_name

client = MotorClient('localhost', 27017)
db = client[database_name]

#@coroutine
#def _login(db):
#    yield db.authenticate("server", " fv7Y0C-gZm4EPFl_KJA")
#    info('%s: Login exitoso!', __name__)
#_login(db)


@coroutine
def stop_db():
    from .message_broker import cursor as msg_broker_cursor
    if msg_broker_cursor:
        yield msg_broker_cursor.close()
    client.disconnect()


class NoObjectReturnedFromDB(Exception):
    def __str__(self):
        return 'Exception: No object returned from ' \
               'database.'
