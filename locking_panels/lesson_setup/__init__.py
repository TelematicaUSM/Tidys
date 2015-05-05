import src

from tornado.gen import coroutine
from tornado.escape import xhtml_escape
from pymongo.errors import DuplicateKeyError
from src.db import Course
from panels.user import UserWSC


class LessonSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'lesson-setup-panel'
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
    @src.wsclass.WSClass.subscribe('getCourses')
    @coroutine
    def send_course_names(self, message):
        try:
            courses = yield Course.get_user_courses(
                self.handler.user)
                
            self.handler.write_message(
                {'type': 'courses',
                 'courses': courses})
                
        except AttributeError:
            if not hasattr(self.handler, 'user'):
                UserWSC.send_user_not_loaded_error(
                    self.handler, message)
                                
    @src.wsclass.WSClass.subscribe('createCourse')
    @coroutine
    def create_course(self, message):
        try:
            course_name = xhtml_escape(message['name'])
            courses = yield Course.create(
                self.handler.user, course_name)
                
            self.handler.write_message(
                {'type': 'createCourseResult',
                 'result': 'ok'})
                
        except AttributeError:
            if not hasattr(self.handler, 'user'):
                UserWSC.send_user_not_loaded_error(
                    self.handler, message)
        
        except DuplicateKeyError:
            self.handler.write_message(
                {'type': 'createCourseResult',
                 'result': 'duplicate'})
