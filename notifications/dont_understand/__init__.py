from tornado.ioloop import IOLoop
from tornado.gen import coroutine

import src
from src.db import ConditionNotMetError
from src.wsclass import subscribe

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
    def __init__(self, handler):
        super().__init__(handler)
        self.timeout_handle = None

    @subscribe('dontUnderstand.counter.changed', 'l')
    def hola(self, message):
        pass

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
            raise########################

    @subscribe('dontUnderstand.start', 'w')
    @coroutine
    def increase_du_counter(self, message=None):
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

        except:
            raise###################
            # couse can not be defined

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

        except ConditionNotMetError:
            pass########################

        except AttributeError:
            if not hasattr(self.handler, 'course'):
                pass
            else:
                raise
