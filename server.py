# -*- coding: UTF-8 -*-

import conf
import panels

from signal import signal, SIGINT
from sys import exit
from logging import debug, info, warning, error, critical

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from src import ui_modules, ui_methods


class AppHandler(RequestHandler):
    def get(self):
        self.render('boxes.html')


app = Application(
    [('/$', AppHandler)],
    debug = conf.debug,
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
