# -*- coding: UTF-8 -*-

import json

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

import conf
from tornado.websocket import WebSocketHandler
from src import ui_modules, ui_methods, messages
from src.boiler_ui_module import BoilerUIModule


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
    path = 'controller.MSGHandler'

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
        messages.code_debug(
            self.path+'.open',
            'New connection established! %s (%s)' %
                (self, self.request.remote_ip)
        )
            
        self.actions = {}
        self.wsobjects = [wsclass(self)
                          for wsclass in self.wsclasses]
        self.__class__.clients.add(self)
        self.__class__.client_count += 1

    def on_message(self, message):
        messages.code_debug(
            self.path+'.on_message',
            'Message arrived: {}.'.format(message)
        )

        try:
            message = json.loads(message)
            
            for action in self.actions[message['type']]:
                IOLoop.current().spawn_callback(action,
                                                message)
        
        except KeyError:
            if 'type' in message:
                self.send_error('wrongMessageType', message,
                                'The client has sent a '
                                'message of an '
                                'unrecognized type.')
            else:
                self.send_malformed_message_error(message)
                 
        except ValueError:
            self.send_malformed_message_error(message)
    
    def send_error(self, critical_type, message,
                   description):
        self.write_message({'type': 'critical',
                            'critical_type': critical_type,
                            'message': message,
                            'description': description})
    
    def send_malformed_message_error(self, message):
        self.send_error('malformedMessage', message,
                        "The client has sent a message "
                        "which either isn't in JSON "
                        "format, does not have a 'type' "
                        "field or at least one attribute "
                        "is not consistent with the "
                        "others.")
    
    def on_close(self):
        self.__class__.clients.remove(self)
        
        messages.code_debug(
            self.path+'.on_close',
            'Connection closed! %s (%s)' %
                (self, self.request.remote_ip)
        )
    
    def write_message(self, message):
        messages.code_debug(
            self.path+'.write_message',
            'Sending message: {}.'.format(message)
        )
        super().write_message(message)


app = Application(
    [('/ws$', MSGHandler),
     ('/(.*)$', GUIHandler),],
    debug=conf.debug,
    static_path='./static',
    template_path='./templates',
    ui_modules=[ui_modules],
    ui_methods=[ui_methods],
)

app.listen(conf.port)

import panels
for module in app.ui_modules.values():
    if issubclass(module, BoilerUIModule):
        module.add_handler(app)
