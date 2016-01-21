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
from src.db import Course, NoObjectReturnedFromDB
from src.wsclass import subscribe


class StudentSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'student-setup-panel'
    classes = {'scrolling-panel', 'student'}
    conf = {
        'static_url_prefix': '/student_setup/',
        'static_path':
            './locking_panels/student_setup/static',
        'js_files': ['student_setup.js'],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/student_setup/'
            'student_setup.html')


class StudentSetupWSC(src.wsclass.WSClass):
    @subscribe('studentSetup.course.set', 'w')
    @coroutine
    def set_course(self, message):
        try:
            user = self.handler.user

            if user.status != 'seat':
                return

            # Load Course
            course = yield Course.get(message['course_id'])
            self.handler.course = course

            # User Assign Course
            yield user.assign_course(course.id)

            self.pub_subs['w'].send_message(
                {'type': 'studentSetup.course.set.ok'})

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
            else:
                raise
