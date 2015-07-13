import re
import src
import panels

from tornado.gen import coroutine
from tornado.escape import xhtml_escape
from pymongo.errors import DuplicateKeyError
from src.db import Course, NoObjectReturnedFromDB
from src.wsclass import subscribe


class LessonSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'lesson-setup-panel'
    classes = {'scrolling-panel', 'room-code-panel'}
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
    @subscribe('getCourses')
    @coroutine
    def send_course_names(self, message):
        try:
            courses = yield Course.get_user_courses(
                self.handler.user)

            self.pub_subs['w'].send_message(
                {'type': 'courses',
                 'courses': courses})

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                usr_wsc = self.handler.ws_objects[
                    panels.user.UserWSC]
                usr_wsc.send_user_not_loaded_error(message)

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

            course = yield Course.create(self.handler.user,
                                         course_name)
            self.pub_subs['w'].send_message(
                {'type': 'createCourseResult',
                 'result': 'ok',
                 'course_id': course.id})

        except KeyError:
            self.handler.send_malformed_message_error(
                message)

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                panels.user.UserWSC.\
                    send_user_not_loaded_error(
                        self.handler, message)

        except DuplicateKeyError:
            self.pub_subs['w'].send_message(
                {'type': 'createCourseResult',
                 'result': 'duplicate'})

    @subscribe('assignCourseToCurrentRoom')
    @coroutine
    def assign_course_to_current_room(self, message):
        try:
            self.handler.course = yield Course(
                message['course_id'])
            room = yield self.handler.room_code.room
            yield room.assign_course(message['course_id'])

            self.pub_subs['w'].send_message(
                {'type': 'courseAssignmentOk'})

        except (KeyError, NoObjectReturnedFromDB):
            self.handler.send_malformed_message_error(
                message)

        except AttributeError:
            if not hasattr(self.handler, 'room_code'):
                panels.user.UserWSC.\
                    send_room_not_loaded_error(
                        self.handler, message)
