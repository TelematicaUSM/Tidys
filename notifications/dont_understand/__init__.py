from tornado.gen import coroutine

import src
from src.db import ConditionNotMetError
from src.wsclass import subscribe


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
    def __init__(self, handler):
        super().__init__(handler)

    @coroutine
    def notify_teacher(self):
        try:
            self.pub_subs['d'].send_message(
                {
                    'type': 'teacherMessage',
                    'content': {}
                }
            )

    @subscribe('dontUnderstand.start', 'w')
    @coroutine
    def increase_du_counter(self):
        try:
            yield self.handler.course.modify(
                {
                    '$inc': {'du_counter': 1}
                }
            )

        except:
            raise

    @subscribe('dontUnderstand.stop', 'w')
    @coroutine
    def decrease_du_counter(self):
        try:
            yield self.handler.course.modify_if(
                {
                    'du_counter': {'$gt': 0}
                },
                {
                    '$inc': {'du_counter': -1}
                }
            )

        except ConditionNotMetError:
            pass

        except AttributeError:
            if not hasattr(self.handler, 'course'):
                pass
            else:
                raise

    @coroutine
    def end(self):
        try:
            yield self.decrease_du_counter()
            yield super().end()

        except:
            raise
