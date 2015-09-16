# -*- coding: UTF-8 -*-

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
