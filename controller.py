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
    @coroutine
    def get(self, room_code):
        try:
            classes = {'system-panel'}
            #room_code must be passed to the template as a
            #handler's attribute, because it is used in the
            #home panel.
            self.room_code = room_code
            
            if room_code:
                c = yield db.Code(room_code)
                
                if c.code_type is db.CodeType.room:
                    classes.update(
                        {'teacher-panel',
                        'room-code-panel'})
                else:
                    classes.update(
                        {'student-panel',
                         'seat-code-panel'})
            else:
                classes.update({'teacher-panel',
                                'student-panel'})
                                
            messages.code_debug('controller.GUIHandler.get',
                                'Rendering boxes.html ...')
            self.render('boxes.html', classes=classes)
            
        except db.NoObjectReturnedFromDB:
            self.render('boxes.html',
                critical='El código escaneado no está '
                         'registrado!')

class LoginHandler(RequestHandler):
    path = 'controller.LoginHandler'
    disc_doc = None     #google's discovery document
    disc_doc_client = httplib2.Http('.disc_doc.cache')
        #https://developers.google.com/api-client-library/
        #python/guide/thread_safety
    
    @coroutine
    def get(self):
        try:
            redirect_uri = urlunparse(
                (self.get_scheme(), self.request.host,
                 conf.login_path, '', '', '')
            )
            #remember the user for a longer period of time
            remember = self.get_argument('remember', False)
            room_code = self.get_argument('room_code',
                                          False)
            state = jwt.encode({'remember': remember,
                                'room_code': room_code},
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
                messages.code_debug(self.path+'.get',
                    'Rendering login.html ...')
                self.render('login.html', token=token)
        
        except oa2_client.FlowExchangeError:
            self.render('boxes.html',
                        classes={'system-panel'},
                        critical='Error de autenticación!')
    
    def get_scheme(self):
        if 'Scheme' in self.request.headers:
            return self.request.headers['Scheme']
        else:
            return self.request.protocol
    
    @property
    def state(self):
        if hasattr(self, '_state'):
            return self._state
        
        state = self.get_argument('state', None)
        
        if state:
            self._state = jwt.decode(state,
                                    secrets['simple'])
        else:
            self._state = None
        
        return self._state
    
    def get_exp(self):
        if self.state:
            delta = conf.long_account_exp \
                    if self.state['remember'] else \
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
        
        if self.disc_doc == None:
            messages.code_debug(code_path,
                'Requesting discovery document ...')
                
            with ThreadPoolExecutor(1) as thread:
                self.__class__.disc_doc = thread.submit(
                    _req_disc_doc)
                self.disc_doc = \
                    yield self.__class__.disc_doc
                #Este yield tiene que ir dentro, ya que el
                #thread no se comenzará a ejecutar si no se
                #yieldea y no se puede comenzar a ejecutar
                #fuera del with ya que ahí no existe ... o
                #algo asi XD :C
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

    def decode_httplib2_json(self, response):
        return json.loads(
            response[1].decode('utf-8')
        )


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


try:
    with open(conf.secrets_file, 'r') as f:
        secrets = json.load(f)
        
    with open(conf.google_secrets_file, 'r') as f:
        google_secrets = json.load(f)

    app = Application(
        [('/ws$', MSGHandler),
         ('/{.login_path}$'.format(conf), LoginHandler),
         ('/([0-9a-z]{5})?$', GUIHandler),],
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
