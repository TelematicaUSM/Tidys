# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from tornado.gen import coroutine
from pymongo.errors import OperationFailure
from motor import MotorClient

from conf import database_name

client = MotorClient('localhost', 27017)
db = client[database_name]

# @coroutine
# def _login(db):
#     yield db.authenticate("server", " fv7Y0C-gZm4El_KJA")
#     info('%s: Login exitoso!', __name__)
# _login(db)


@coroutine
def stop_db():
    from .message_broker import cursor as msg_broker_cursor
    if msg_broker_cursor:
        yield msg_broker_cursor.close()
    client.disconnect()


class NoObjectReturnedFromDB(Exception):

    """Rise when an object was not found in the database.

    The first argument should be a DBObject subclass.
    """


class ConditionNotMetError(OperationFailure):

    """Raise when a database conditional operation fails.

    A conditional operation queries for a document id and a
    condition. This kind of operations fail when the
    condition is not met or when the document no longer
    exists.

    The ``details`` keyword argument is the complete error
    document returned by the server.
    """

    def __init__(self, message='', *args, **kwargs):
        super().__init__(
            message or 'The condition was not met or this '
            'object no longer exists on the database.',
            *args,
            **kwargs
        )
