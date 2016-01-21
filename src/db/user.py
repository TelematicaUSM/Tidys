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


"""User mongodb adapter

Users have a status (student or teacher) and location (room,
seat).
"""

from tornado.gen import coroutine

from src.utils import random_word
from .common import db, ConditionNotMetError
from .db_object import DBObject


class User(DBObject):
    coll = db.users
    defaults = {
        'instances': 0,         # number of tabs opened
        'status': 'none',       # current user status
        'room_code': 'none',    # last scanned room code
        'room_name': None,      # current room name
        'course_id': None,      # current course ID
        'seat_id': None,        # current seat ID
    }

    @classmethod
    @coroutine
    def from_google_userinfo(cls, userinfo):
        """Create a User object from google's userinfo data.

        Sample userinfo data::

            {'family_name': 'Ganter',
             'given_name': 'Cristóbal',
             'kind': 'plus#personOpenIdConnect',
             'locale': 'es',
             'name': 'Cristóbal Ganter',
             'picture': 'https://lh4.googleusercontent.com/
                         -HDGdhHDjlh/AAAAAAAAAAI/
                         LJGDDJHK765K/-Nuvyyib864/photo.jpg?
                         sz=50',
             'profile': 'https://plus.google.com/
                         738259437132941462401',
             'sub': '738259437132941462401'}
        """
        yield cls.coll.update(
            {'_id': userinfo['sub']},
            {
                '$set': {'google_userinfo': userinfo}
            },
            upsert=True)
        self = yield cls.get(userinfo['sub'])
        return self

    @classmethod
    @coroutine
    def get_name(cls, id_):
        """Return the name of a user.

        :param str id_:
            The ID of the user.

        :return:
            A future that resolves to a string.

        .. todo::
            -   Generalize this method to obtain many names
                at once.
        """
        try:
            result = yield cls.coll.find_one(
                id_,
                fields={
                    '_id': False,
                    'google_userinfo.name': True,
                }
            )
            return result['google_userinfo']['name']

        except:
            raise

    def __str__(self):
        return self.name

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

    @coroutine
    def increase_instances(self):
        yield self.modify(
            {
                '$inc': {'instances': 1}
            }
        )

    @coroutine
    def decrease_instances(self):
        """Decrease the ``instances`` counter of the user.

        :raises OperationFailure:
            If an error occurred during the update
            operation.
        """
        try:
            yield self.modify_if(
                {
                    'instances': {'$gt': 0}
                },
                {
                    '$inc': {'instances': -1}
                }
            )
            yield self.reset_if(
                {'instances': 0}, 'status', 'course_id')

        except ConditionNotMetError:
            pass

    @coroutine
    def assign_course(self, course_id):
        """Assign a ``course_id`` to this user.

        The default value of ``course_id`` is ``None``,
        which indicates that this user has no associated
        course.

        :param str course_id:
            The course ID to be associated with this user.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.
        """
        yield self.store('course_id', course_id)

    @coroutine
    def deassign_course(self, if_last_instance=False):
        """Set this user's ``course_id`` to ``None``.

        The default value of ``course_id`` is ``None``,
        which indicates that this user has no associated
        course.

        :param bool if_last_instance:
            If ``True``, the course will only be deassigned
            if this is the last instance of the user.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.

        :raises OperationFailure:
            If an error occurred during the update
            operation.
        """
        try:
            condition = \
                {'instances': 1} if if_last_instance else {}

            yield self.reset_if(condition, 'course_id')

        except ConditionNotMetError:
            pass
