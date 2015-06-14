# -*- coding: UTF-8 -*-

import json
from datetime import datetime, timedelta
from functools import partialmethod
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlunparse

import jwt
import httplib2
from tornado.gen import coroutine
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from oauth2client import client as oa2_client

import conf
from src import ui_modules, ui_methods, messages as msg, db
from src.boiler_ui_module import BoilerUIModule
from src.pub_sub import OwnerPubSub, NoMessageTypeError, \
    UnrecognizedMessageError

_path = 'controller'


class GUIHandler(RequestHandler):
    @coroutine
    def get(self, room_code):
        try:
            classes = {'system-panel'}
            # room_code must be passed to the template as a
            # handler's attribute, because it is used in the
            # home panel.
            self.room_code = room_code

            if room_code:
                c = yield db.Code(room_code)

                if c.code_type is db.CodeType.room:
                    classes.update(
                        {'teacher-panel', 'room-code-panel'}
                    )
                else:
                    classes.update(
                        {'student-panel',
                         'seat-code-panel'})
            else:
                classes.update({'teacher-panel',
                                'student-panel'})

            msg.code_debug('controller.GUIHandler.get',
                           'Rendering boxes.html ...')
            self.render('boxes.html', classes=classes)

        except db.NoObjectReturnedFromDB:
            self.render(
                'boxes.html',
                critical='El código escaneado no está '
                         'registrado!'
            )


class LoginHandler(RequestHandler):
    _path = msg.join_path(_path, 'LoginHandler')
    disc_doc = None     # google's discovery document
    disc_doc_client = httplib2.Http('.disc_doc.cache')
    # https://developers.google.com/api-client-library/
    # python/guide/thread_safety

    @coroutine
    def get(self):
        _path = msg.join_path(self._path, 'get')
        try:
            redirect_uri = urlunparse(
                (self.get_scheme(), self.request.host,
                 conf.login_path, '', '', '')
            )
            # remember the user for a longer period of time
            remember = self.get_argument('remember', False)
            room_code = self.get_argument('room_code',
                                          False)
            state = jwt.encode({'remember': remember,
                                'room_code': room_code},
                               secrets['simple'])
            flow = oa2_client.OAuth2WebServerFlow(
                google_secrets['web']['client_id'],
                google_secrets['web']['client_secret'],
                scope='openid profile',
                redirect_uri=redirect_uri,
                state=state)

            auth_code = self.get_argument('code', False)

            if not auth_code:
                auth_uri = flow.step1_get_authorize_url()
                self.redirect(auth_uri)

            else:
                with ThreadPoolExecutor(1) as thread:
                    credentials = yield thread.submit(
                        flow.step2_exchange, auth_code)
                # Intercambiar el codigo antes que nada para
                # evitar ataques

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
                # https://developers.google.com/+/api/
                # openidconnect/getOpenIdConnect

                user = yield db.User.from_google_userinfo(
                    userinfo)
                token = jwt.encode({'id': user.id,
                                    'exp': self.get_exp()},
                                   user.secret)
                msg.code_debug(_path,
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
        _path = msg.join_path(self._path,
                              'request_disc_doc')

        def _req_disc_doc():
            dd = self.disc_doc_client.request(
                'https://accounts.google.com/.well-known/'
                'openid-configuration', 'GET')
            return self.decode_httplib2_json(dd)

        if self.disc_doc is None:
            msg.code_debug(
                _path, 'Requesting discovery document ...')

            with ThreadPoolExecutor(1) as thread:
                self.__class__.disc_doc = thread.submit(
                    _req_disc_doc)
                self.disc_doc = \
                    yield self.__class__.disc_doc
                # Este yield tiene que ir dentro, ya que el
                # thread no se comenzará a ejecutar si no se
                # yieldea y no se puede comenzar a ejecutar
                # fuera del with ya que ahí no existe ... o
                # algo asi XD :C
                self.__class__.disc_doc = None
                msg.code_debug(
                    _path, 'self.__class__.disc_doc = None')

            msg.code_debug(_path,
                           'Discovery document arrived!')

        else:
            msg.code_debug(
                _path, 'Waiting for discovery document ...')

            self.disc_doc = yield self.disc_doc
            msg.code_debug(_path,
                           'Got the discovery document!')

    def decode_httplib2_json(self, response):
        return json.loads(
            response[1].decode('utf-8')
        )


class MSGHandler(WebSocketHandler):
    _path = msg.join_path(_path, 'MSGHandler')

    ws_classes = []
    clients = set()
    client_count = 0    # Total clients that have connected

    def initialize(self):
        _path = msg.join_path(self._path, 'initialize')
        msg.code_debug(
            _path,
            'New connection established! {0} '
            '({0.request.remote_ip})'.format(self)
        )

        self.local_pub_sub = OwnerPubSub(
            name='local_pub_sub')

        self.ws_pub_sub = OwnerPubSub(
            name='ws_pub_sub',
            send_function=self.write_message
        )
        self.ws_objects = [ws_class(self)
                           for ws_class in self.ws_classes]

        self.__class__.clients.add(self)
        self.__class__.client_count += 1

    @classmethod
    def add_class(cls, wsclass):
        cls.ws_classes.append(wsclass)

    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.write_message(message)

    def on_message(self, message):
        """Process messages when they arrive.

        :param str message:
            The received message. This should be a valid
            json document.

        .. todo::
            * Review error handling.
        """
        _path = msg.join_path(self._path, 'on_message')
        msg.code_debug(
            _path,
            'Message arrived: {}.'.format(message)
        )

        try:
            # Throws ValueError
            message = json.loads(message)

            self.ws_pub_sub.execute_actions(message)

        except (ValueError, NoMessageTypeError):
            self.send_malformed_message_error(message)
            msg.malformed_message(_path, message)

        except UnrecognizedMessageError:
            self.send_error(
                'unrecognizedMessage',
                message,
                "The client has sent a message for which "
                "there is no associated action."
            )
            msg.unrecognized_message_type(_path, message)

    def send_error(self, critical_type, message,
                   description):
        self.write_message(
            {'type': 'critical',
             'critical_type': critical_type,
             'message': message,
             'description': description}
        )

    send_malformed_message_error = partialmethod(
        send_error,
        'malformedMessage',
        description="The client has sent a message which "
                    "either isn't in JSON format, does not "
                    "have a 'type' field or at least one "
                    "attribute is not consistent with the "
                    "others."
    )

    def on_close(self):
        _path = msg.join_path(self._path, 'on_close')

        for ws_object in self.ws_objects:
            ws_object.unregister()

        self.__class__.clients.discard(self)

        msg.code_debug(
            _path,
            'Connection closed! {0} '
            '({0.request.remote_ip})'.format(self)
        )


try:
    with open(conf.secrets_file, 'r') as f:
        secrets = json.load(f)

    with open(conf.google_secrets_file, 'r') as f:
        google_secrets = json.load(f)

    app = Application(
        [('/ws$', MSGHandler),
         ('/{.login_path}$'.format(conf), LoginHandler),
         ('/([0-9a-z]{5})?$', GUIHandler), ],
        debug=conf.debug,
        static_path='./static',
        template_path='./templates',
        ui_modules=[ui_modules],
        ui_methods=[ui_methods],
    )

    app.listen(conf.port)

    # Import the modules which register actions in the
    # MSGHandler
    import backend_modules
    import locking_panels
    import notifications
    import panels

    # BoilerUIModules that aren't automatically loaded from
    # a package, must add their handlers to the app.
    for module in app.ui_modules.values():
        if issubclass(module, BoilerUIModule):
            module.add_handler(app)

except FileNotFoundError as e:
    if e.filename in (conf.secrets_file,
                      conf.google_secrets_file):
        desc = "Couldn't find the secrets file: " \
            "{.filename}. Change your configuration in " \
            "conf/__init__.py or create the file. " \
            "For more information, see the " \
            "documentation.".format(e)
        raise FileNotFoundError(e.errno, desc) from e
    else:
        raise
