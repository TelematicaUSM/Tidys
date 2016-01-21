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


import re

from tornado.gen import coroutine
from tornado.escape import xhtml_escape
from pymongo.errors import DuplicateKeyError

import src
from src.db import Course, NoObjectReturnedFromDB
from src.wsclass import subscribe


class LessonSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'lesson-setup-panel'
    classes = {'scrolling-panel', 'teacher'}
    conf = {
        'static_url_prefix': '/lesson_setup/',
        'static_path':
            './locking_panels/lesson_setup/static',
        'css_files': ['lesson_setup.css'],
        'js_files': ['lesson_setup.js'],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/lesson_setup/'
            'lesson_setup.html')


class LessonSetupWSC(src.wsclass.WSClass):
    @subscribe('createCourse')
    @coroutine
    def create_course(self, message):
        try:
            course_name = xhtml_escape(message['name'])

            if not re.search('\S', course_name):
                self.pub_subs['w'].send_message(
                    {'type': 'createCourseResult',
                     'result': 'emptyName'})
                return

            course = yield Course.create(
                self.handler.user, course_name)

            self.pub_subs['w'].send_message(
                {
                    'type': 'createCourseResult',
                    'result': 'ok',
                    'course_id': course.id
                }
            )

        except KeyError:
            self.handler.send_malformed_message_error(
                message)

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                self.handler.send_user_not_loaded_error(
                    message)

        except DuplicateKeyError:
            self.pub_subs['w'].send_message(
                {'type': 'createCourseResult',
                 'result': 'duplicate'})

    @subscribe('course.assignment.to_room', 'w')
    @coroutine
    def assign_course_to_current_room(self, message):
        try:
            user = self.handler.user

            if user.status != 'room':
                return

            # Load Course
            course = yield Course.get(message['course_id'])
            self.handler.course = course

            # Room Deasign Course
            if user.course_id is not None:
                self.handler.room.deassign_course(
                    user.course_id)

            # Room Assign Course
            room = yield self.handler.room_code.room
            yield room.assign_course(course.id)

            # User Assign Course
            yield user.assign_course(course.id)

            self.course_assignment_source = True
            """This variable identifies the source of the
            ``course.assignment.ok`` message."""

            self.pub_subs['d'].send_message(
                {
                    'type': self.handler.user_msg_type,
                    'content': {
                        'type': 'course.assignment.ok'
                    }
                }
            )

        except KeyError:
            if 'course_id' not in message:
                self.handler.send_malformed_message_error(
                    message)
            else:
                raise

        except NoObjectReturnedFromDB:
            self.handler.send_malformed_message_error(
                message)

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                self.handler.send_user_not_loaded_error(
                    message)

            elif not hasattr(self.handler, 'room_code') or \
                    self.handler.room_code is None:
                self.handler.send_room_not_loaded_error(
                    message)

            else:
                raise

    @subscribe('course.assignment.ok', 'l')
    @coroutine
    def sync_course_id_and_forward_to_client(self, message):
        if not (hasattr(self, 'course_assignment_source')
                and self.course_assignment_source):

            yield self.handler.user.sync('course_id')
            course_id = self.handler.user.course_id

            if course_id is not None:
                self.handler.course = yield Course.get(
                    course_id)

        self.pub_subs['w'].send_message(
            {'type': 'course.assignment.ok'})
