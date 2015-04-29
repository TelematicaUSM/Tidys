import src

from tornado.gen import coroutine
from src.db import Course


class LessonSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'lesson-setup-panel'
    classes = {'scrolling-panel', 'teacher-panel'}
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
            courses = yield Course.get_user_course_names(
                self.handler.user)
                
            self.handler.write_message(
                {'type': 'courses',
                 'courses': courses})
                
        except AttributeError:
            if not hasattr(self.handler, 'user'):
                #FIXME: duplicate error message in user
                #       panel
                self.send_error('userNotLoaded', message,
                                'There was no loaded user '
                                'when this message '
                                'arrived.')
