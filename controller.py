# -*- coding: UTF-8 -*-

import conf, json

from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from src import ui_modules, ui_methods
from src.boiler_ui_module import BoilerUIModule
from logging import debug


class GUIHandler(RequestHandler):
    def get(self):
        self.render('boxes.html')


class MSGHandler(WebSocketHandler):
    wsclasses = []

    @classmethod
    def add_class(cls, wsclass):
        cls.wsclasses.append(wsclass)
    
    def register_action(self, msg_type, action):
        if msg_type in self.actions:
            self.actions[msg_type].add(action)
        else:
            self.actions[msg_type] = {action}
    
    def open(self):
        debug('controller.MSGHandler.open: '
              'New connection established!')
        self.actions = {}
        self.wsobjects = [wsclass(self)
                          for wsclass in self.wsclasses]
        
    def on_message(self, message):
        debug('controller.MSGHandler.on_message: '
              'Message arrived: %r.' % message)
              
        message = json.loads(message)
        
        for action in self.actions[message['type']]:
            action(message)


app = Application(
    [('/$', GUIHandler),
     ('/ws$', MSGHandler)],
    debug = conf.debug,
    static_path = './static',
    template_path = './templates',
    ui_modules = [ui_modules,],
    ui_methods = [ui_methods],
)

for module in app.ui_modules.values():
    if issubclass(module, BoilerUIModule):
        module.add_handler(app)
