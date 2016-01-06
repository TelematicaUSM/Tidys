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


from tornado.ioloop import IOLoop
from tornado.gen import coroutine

import src
from src.db import ConditionNotMetError
from src.wsclass import subscribe
from backend_modules.courses import CourseIsNotDefined

DURATION = 1 * 60


class DontUnderstandIndicator(
        src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/dont_understand/',
        'static_path': './notifications/'
                       'dont_understand/static',
        'css_files': ['dont_understand.css'],
        'js_files': ['dont_understand.js'],
    }

    def render(self):
        return self.render_string(
            '../notifications/dont_understand/'
            'dont_understand.html')


class DontUnderstandWSC(src.wsclass.WSClass):
    """

    .. todo::
        *   Maybe the explicit database operations of this
            class should be implemented as patches to the
            corresponding database objects.
    """
    def __init__(self, handler):
        super().__init__(handler)

        self.timeout_handle = None
        """Handle for the
        :meth:`~DontUnderstandWSC.decrease_du_counter`
        callback."""

    @subscribe('dontUnderstand.counter.changed', 'l')
    @coroutine
    def update_teacher_icon(self, message):
        """Send a message to update the icon's state.

        This coroutine sends a message with the following
        format:

        .. code-block:: json

            {
                "type": "dontUnderstand.icon.state.set",
                "proportion": 0.5
            }

        Where ``"proportion"`` is the ratio between the
        students that dont understand and all the students
        that are currently participating in this course.

        :raises OperationFailure:
            On a database error.
        """
        try:
            course = self.handler.course

            yield course.sync('du_counter')
            du = course.du_counter
            total = yield course.count_students()
            proportion = du/total if total > 0 else 0

            self.pub_subs['w'].send_message(
                {
                    'type': 'dontUnderstand.icon.state.set',
                    'proportion': proportion
                }
            )
        except AttributeError as ae:
            h = self.handler

            if h.course is None:
                raise CourseIsNotDefined from ae

            elif not hasattr(h.course, 'du_counter'):
                e = AttributeError(
                    "The coroutine has attempted to access "
                    "the attribute `du_counter` of the "
                    "course, but the course didn't have "
                    "the attribute. This should never "
                    "happen.")
                raise e from ae

            else:
                raise

        except:
            raise

    @coroutine
    def notify_teacher(self):
        try:
            self.pub_subs['d'].send_message(
                {
                    'type': self.handler.course_msg_type,
                    'content': {
                        'type': 'teacherMessage',
                        'content': {
                            'type':
                                'dontUnderstand.counter.'
                                'changed'
                        }
                    }
                }
            )
        except:
            raise

    @subscribe('dontUnderstand.start', 'w')
    @coroutine
    def increase_du_counter(self, message=None):
        """Increase the don't understand counter.

        :param message:
            The message that triggered the execution of this
            method.
        :type message: dict or None

        :raises ConditionNotMetError:
            If the current course no longer exists in the
            database. This should never happen!
        """
        try:
            if self.timeout_handle is None:
                yield self.handler.course.modify(
                    {
                        '$inc': {'du_counter': 1}
                    }
                )

                self.timeout_handle = \
                    IOLoop.current().call_later(
                        DURATION, self.decrease_du_counter)
                yield self.notify_teacher()

        except AttributeError as ae:
            if self.handler.course is None:
                raise CourseIsNotDefined from ae

            else:
                raise

        except ConditionNotMetError as cnme:
            e = ConditionNotMetError(
                'The current course no longer exist in the '
                'database. This should never happen!')
            raise e from cnme

        except:
            raise

    @subscribe('dontUnderstand.stop', 'w')
    @coroutine
    def decrease_du_counter(self, message=None):
        try:
            if self.timeout_handle is not None:
                yield self.handler.course.modify_if(
                    {
                        'du_counter': {'$gt': 0}
                    },
                    {
                        '$inc': {'du_counter': -1}
                    }
                )

                IOLoop.current().remove_timeout(
                    self.timeout_handle)
                self.timeout_handle = None
                yield self.notify_teacher()

        except AttributeError as ae:
            if self.handler.course is None:
                raise CourseIsNotDefined from ae

            else:
                raise

        except ConditionNotMetError:
            pass

        except:
            raise
