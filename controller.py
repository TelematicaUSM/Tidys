# -*- coding: UTF-8 -*-

import conf

from tornado.web import Application, RequestHandler
from src import ui_modules, ui_methods


class AppHandler(RequestHandler):
    def get(self):
        content = '<span style="margin:3rem; ' \
                               'display:block;' \
                               'text-align:center;">' \
                      'TornadoBoiler is a set of files ' \
                      'which serve me as a base to start ' \
                      'new Tornado projects.' \
                  '</span>'
        self.render('layout.html', raw_content=True,
                    content=content)


app = Application(
    [('/$', AppHandler)],
    debug = conf.debug,
    static_path = './static',
    template_path = './templates',
    ui_modules = [ui_modules],
    ui_methods = [ui_methods],
)
