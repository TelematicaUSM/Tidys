# -*- coding: UTF-8 -*-

import conf, json, jwt
from sys import exit
from datetime import datetime, timedelta
from logging import debug, error, critical
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlunparse

from tornado.gen import coroutine
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

import httplib2
from oauth2client import client as oa2_client

from src import ui_modules, ui_methods, messages, db
from src.boiler_ui_module import BoilerUIModule


class GUIHandler(RequestHandler):
    def get(self):
        self.render('boxes.html')


class LoginHandler(RequestHandler):
    disc_doc = None     #google's discovery document
    disc_doc_client = httplib2.Http('.disc_doc.cache')
        #https://developers.google.com/api-client-library/
        #python/guide/thread_safety
    
    @coroutine
    def get(self):
        try:
            redirect_uri = urlunparse(
                (self.get_scheme(), self.request.host,
                 'login', '', '', '')
            )
            #remember the user for a longer period of time
            remember = self.get_argument('remember',
                                         False)
            state = jwt.encode({'remember': remember},
                               secrets['simple'])
            flow = oa2_client.OAuth2WebServerFlow(
                google_secrets['web']['client_id'],
                google_secrets['web']['client_secret'],
                scope = 'openid profile',
                redirect_uri = redirect_uri,
                state = state)
            
            auth_code = self.get_argument('code', False)
            
            if not auth_code:
                auth_uri = flow.step1_get_authorize_url()
                self.redirect(auth_uri)

            else:
                with ThreadPoolExecutor(1) as thread:
                    credentials = yield thread.submit(
                        flow.step2_exchange, auth_code)
                #Intercambiar el codigo antes que nada para
                #evitar ataques
                
                yield self.request_disc_doc()
                
                userinfo_endpoint = \
                    self.disc_doc['userinfo_endpoint']
                    
                http_auth = credentials.authorize(
                    httplib2.Http())
                    
                with ThreadPoolExecutor(1) as thread:
                    userinfo = yield thread.submit(
                        http_auth.request,
                        userinfo_endpoint)
                userinfo = self.decode_httplib2_json(
                    userinfo)
                #https://developers.google.com/+/api/
                #openidconnect/getOpenIdConnect
                
                user = yield db.User.from_google_userinfo(
                    userinfo)
                token = jwt.encode({'id': user.id,
                                    'exp': self.get_exp()},
                                   user.secret)
                self.render('login.html', token=token)
        except:
            messages.unexpected_error(
                'controller.LoginHandler.get')
            raise
    
    def get_scheme(self):
        if 'Scheme' in self.request.headers:
            return self.request.headers['Scheme']
        else:
            return self.request.protocol
    
    def get_exp(self):
        state = self.get_argument('state', None)
        
        if state:
            state_dict = jwt.decode(state,
                                    secrets['simple'])
            delta = conf.long_account_exp \
                    if state_dict['remember'] else \
                    conf.short_account_exp
            return datetime.utcnow() + timedelta(**delta)
        else:
            return conf.short_account_exp
    
    @coroutine
    def request_disc_doc(self):
        code_path = \
            'controller.LoginHandler.request_disc_doc'
        
        def _req_disc_doc():
            dd = self.disc_doc_client.request(
                'https://accounts.google.com/.well-known/'
                'openid-configuration', 'GET')
            return self.decode_httplib2_json(dd)
            
        try:
            if self.disc_doc == None:
                messages.code_debug(code_path,
                    'Requesting discovery document ...')
                    
                with ThreadPoolExecutor(1) as thread:
                    self.__class__.disc_doc = thread.submit(
                        _req_disc_doc)
                    self.disc_doc = \
                        yield self.__class__.disc_doc
                    #Este yield tiene que ir dentro, ya que
                    #el thread no se comenzará a ejecutar si
                    #no se yieldea y no se puede comenzar a
                    #ejecutar fuera del with ya que ahí no
                    #existe ... o algo asi XD :C
                    self.__class__.disc_doc = None
                    messages.code_debug(code_path,
                        'self.__class__.disc_doc = None')
                    
                messages.code_debug(code_path,
                    'Discovery document arrived!')
                
            else:
                messages.code_debug(code_path,
                    'Waiting for discovery document ...')
                self.disc_doc = yield self.disc_doc
                messages.code_debug(code_path,
                    'Got the discovery document!')
                    
        except:
            messages.unexpected_error(
                'controller.LoginHandler.request_disc_doc')
            raise

    def decode_httplib2_json(self, response):
        return json.loads(
            response[1].decode('utf-8')
        )


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
        messages.code_debug('controller.MSGHandler.open',
                   'New connection established!')
        self.actions = {}
        self.wsobjects = [wsclass(self)
                          for wsclass in self.wsclasses]
        self.__class__.clients.add(self)
        self.__class__.client_count += 1

    def on_message(self, message):
        messages.code_debug('controller.MSGHandler.on_message',
                   'Message arrived: %r.' % message)
              
        message = json.loads(message)
        
        for action in self.actions[message['type']]:
            action(message)
    
    def on_close(self):
        MSGHandler.clients.remove(self)


try:
    with open(conf.secrets_file, 'r') as f:
        secrets = json.load(f)
        
    with open(conf.google_secrets_file, 'r') as f:
        google_secrets = json.load(f)

    app = Application(
        [('/$', GUIHandler),
         ('/ws$', MSGHandler),
         ('/login$', LoginHandler),],
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

except FileNotFoundError as error:
    if error.filename == conf.secrets_file:
        messages.file_not_found(code_path='controller',
                                file_name=error.filename,
                                print_f=critical)
        messages.closing()
        exit(1)
    else:
        raise
