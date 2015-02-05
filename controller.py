# -*- coding: UTF-8 -*-

import conf, json, jwt

from sys import exit, exc_info
from datetime import datetime, timedelta
from logging import debug, critical
from urllib.parse import urljoin
from tornado.gen import coroutine
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.auth import GoogleOAuth2Mixin
from src import ui_modules, ui_methods, messages, db
from src.boiler_ui_module import BoilerUIModule


class GUIHandler(RequestHandler):
    def get(self):
        self.render('boxes.html')


class LoginHandler(RequestHandler, GoogleOAuth2Mixin):
    @coroutine
    def get(self):
        try:
            redirect_uri = urljoin(
                self.get_scheme() + '://' +
                self.request.host, 'login')
            debug('LoginHandler.get: '
                      'redirect_uri = %s', redirect_uri)
                           
            if self.get_argument('code', False):
                google_data = \
                    yield self.get_authenticated_user(
                        redirect_uri=redirect_uri,
                        code=self.get_argument('code'))
                user = yield db.User.from_google_data(
                    google_data)
                exp = datetime.utcnow() + \
                      timedelta(days=30) \
                      if not conf.debug else \
                      datetime.utcnow() + \
                      timedelta(minutes=5)
                token = jwt.encode({'id': user.id,
                                    'exp': exp},
                                   user.secret)
                self.render('login.html', token=token)
            else:
                yield self.authorize_redirect(
                    redirect_uri=redirect_uri,
                    client_id=
                       self.settings['google_oauth']['key'],
                    scope=['profile', 'email'],
                    response_type='code',
                    extra_params=
                        {'approval_prompt': 'auto'})
        except:
            error('controller.LoginHandler.get: '
                  'Unexpected error: %s', exc_info()[0])
            raise
    
    def get_scheme(self):
        if 'Scheme' in self.request.headers:
            return self.request.headers['Scheme']
        else:
            return self.request.protocol


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

try:
    with open(conf.secrets_file, 'r') as f:
        file_content = f.read()
    secrets = json.loads(file_content)
    google_oauth = secrets['google']

    app = Application(
        [('/$', GUIHandler),
         ('/ws$', MSGHandler),
         ('/login$', LoginHandler),],
        debug = conf.debug,
        static_path = './static',
        template_path = './templates',
        ui_modules = [ui_modules,],
        ui_methods = [ui_methods],
        login_url = 'login',
        google_oauth = google_oauth,
    )
    
    app.listen(conf.port)

    import panels
    for module in app.ui_modules.values():
        if issubclass(module, BoilerUIModule):
            module.add_handler(app)

except FileNotFoundError as error:
    if error.filename == conf.secrets_file:
        messages.file_not_found(critical, 'controller',
                                error.filename)
        messages.closing()
        exit(1)
    else:
        raise
