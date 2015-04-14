# -*- coding: UTF-8 -*-

import conf, json

from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from src import ui_modules, ui_methods
from src.boiler_ui_module import BoilerUIModule
from logging import debug


class GUIHandler(RequestHandler):
    def get(self, _class):
        if _class:
            self.render('boxes.html',
                        classes={_class, 'system-panel'})
        else:
            self.render('boxes.html')


class MSGHandler(WebSocketHandler):
    wsclasses = []
    clients = set()
    client_count = 0

    @classmethod
    def add_class(cls, wsclass):
        cls.wsclasses.append(wsclass)
    
    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.write_message(message)
    
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
        MSGHandler.clients.add(self)
        MSGHandler.client_count += 1

    def on_message(self, message):
        debug('controller.MSGHandler.on_message: '
              'Message arrived: %r.' % message)
              
        message = json.loads(message)
        
        for action in self.actions[message['type']]:
            action(message)
    
    def on_close(self):
        MSGHandler.clients.remove(self)


app = Application(
    [('/ws$', MSGHandler),
     ('/(.*)$', GUIHandler),],
    debug = conf.debug,
    static_path = './static',
    template_path = './templates',
    ui_modules = [ui_modules],
    ui_methods = [ui_methods],
)

app.listen(conf.port)

import panels
for module in app.ui_modules.values():
    if issubclass(module, BoilerUIModule):
        module.add_handler(app)
