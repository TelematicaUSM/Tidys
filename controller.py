# -*- coding: UTF-8 -*-

import conf

from tornado.web import Application, RequestHandler
from src import ui_modules, ui_methods
from src.boiler_ui_module import BoilerUIModule


class AppHandler(RequestHandler):
    def get(self):
        self.render('boxes.html')


app = Application(
    [('/$', AppHandler)],
    debug = conf.debug,
    static_path = './static',
    template_path = './templates',
    ui_modules = [ui_modules,],
    ui_methods = [ui_methods],
)

for module in app.ui_modules.values():
    if issubclass(module, BoilerUIModule):
        module.add_handler(app)
