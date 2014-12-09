# -*- coding: UTF-8 -*-

import conf

from signal import signal, SIGINT
from sys import exit
from logging import debug, info, warning, error, critical

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from src import ui_modules, ui_methods
from src.handlers import FileGoupsHandler


class AppHandler(RequestHandler):
    def get(self):
        content = '<span style="margin:3rem; ' \
                               'display:block;' \
                               'text-align:center;">' \
                      'TornadoBoiler is a set of files' \
                      'which serve me as a base to start' \
                      'new Tornado projects.' \
                  '</span>'
        self.render('layout.html', raw_content=True,
                    content=content)


app = Application(
    [('/$', AppHandler)],
    debug = conf.debug,
    static_handler_class = FileGoupsHandler,
    static_path = './static',
    template_path = './templates',
    ui_modules = [ui_modules],
    ui_methods = [ui_methods],
)
   
def exit_handler(signal, frame):
    info('\n%s: Closing ...', __name__)
    exit(0)
signal(SIGINT, exit_handler)

port = conf.port
info('%s: Starting on port %d ...', __name__, port)
app.listen(port)
IOLoop.instance().start()
