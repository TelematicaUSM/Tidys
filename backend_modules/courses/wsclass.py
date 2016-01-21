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

import src
from src.wsclass import subscribe
from src.db import Course, User


class CoursesWSC(src.wsclass.WSClass):
    @subscribe('courses.room.get', 'w')
    @coroutine
    def send_room_courses(self, message):
        """Send current room's courses to the client.

        This method is subscribed to the
        ``courses.room.get`` message type.

        The ``user_id`` field of each course is replaced by
        the ``owner`` field. The ``owner`` field contains
        the name of the user, instead of it's ID.

        :param dict message:
            The client's message that executed this method.

        .. todo::
            *   To get the user's names, only one query
                should be made.
                Like: ``User.get_names(id_list)``
        """
        try:
            courses = yield Course.get_courses_from_ids(
                self.handler.room.courses)

            ids = {c['user_id'] for c in courses}
            names = yield {
                id_: User.get_name(id_) for id_ in ids}

            for course in courses:
                course['owner'] = names[
                    course['user_id']
                ]
                del course['user_id']

            self.pub_subs['w'].send_message(
                {'type': 'courses',
                 'courses': courses})

        except AttributeError:
            if not hasattr(self.handler, 'room') or \
                    self.handler.room is None:
                self.handler.send_room_not_loaded_error(
                    message)

            elif not hasattr(self.handler.room, 'courses'):
                """This should never happen again :P."""
                raise

            else:
                raise

    @subscribe('courses.user.get', 'w')
    @coroutine
    def send_user_courses(self, message):
        """Send current user's courses to the client.

        This method is subscribed to the
        ``courses.user.get`` message type.

        :param dict message:
            The client's message that executed this method.
        """
        try:
            courses = yield Course.get_user_courses(
                self.handler.user)

            self.pub_subs['w'].send_message(
                {'type': 'courses',
                 'courses': courses})

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                self.handler.send_user_not_loaded_error(
                    message)

            else:
                raise
