# -*- coding: UTF-8 -*-

"""Render the user panel and process all user messages.

This module patches the :class:`controller.MSGHandler`
class, adding the
:meth:`controller.MSGHandler.send_user_not_loaded_error` and
:meth:`controller.MSGHandler.send_room_not_loaded_error`
methods.
"""

from functools import partialmethod

import jwt
from tornado.gen import coroutine

import src
from controller import MSGHandler
from src import messages as msg
from src.db import User, Code, NoObjectReturnedFromDB
from src.wsclass import subscribe

_path = msg.join_path('panels', 'user')

MSGHandler.send_user_not_loaded_error = partialmethod(
    MSGHandler.send_error,
    'userNotLoaded',
    description='There was no loaded user when '
                'this message arrived.'
)

MSGHandler.send_room_not_loaded_error = partialmethod(
    MSGHandler.send_error,
    'roomNotLoaded',
    description='There was no loaded room when '
    'this message arrived.'
)


class UserPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'user-panel'
    classes = {'scrolling-panel', 'system-panel'}
    name = 'Usuario'
    conf = {
        'static_url_prefix': '/user/',
        'static_path': './panels/user/static',
        'css_files': ['user.css'],
        'js_files': ['user.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/user/user.html')


class UserWSC(src.wsclass.WSClass):

    """Process user messages"""

    _path = msg.join_path(_path, 'UserWSC')

    @subscribe('sessionToken', channels={'w'})
    @coroutine
    def check_token(self, message):
        try:
            uid = jwt.decode(message['token'],
                             verify=False)['id']
            user = yield User(uid)
            jwt.decode(message['token'], user.secret)
            self.handler.user = user
            self.pub_subs['w'].send_message(
                {'type': 'tokenOk'})

            user_msg_type = 'userMessage({})'.format(uid)
            self.register_action_in(
                user_msg_type,
                action=self.route_db_message,
                channels={'d'}
            )

        except (jwt.ExpiredSignatureError, jwt.DecodeError,
                NoObjectReturnedFromDB):
            self.pub_subs['w'].send_message(
                {'type': 'logout'})

    @subscribe('getUserName')
    def get_user_name(self, message):
        try:
            name = self.handler.user.name
            self.pub_subs['w'].send_message(
                {'type': 'userName',
                 'name': name})
        except AttributeError:
            self.send_user_not_loaded_error(message)

    @subscribe('roomCode')
    @coroutine
    def load_room_code(self, message):
        try:
            room_code = yield Code(message['room_code'])
            self.handler.room_code = room_code
            self.handler.room = yield room_code.room
            self.pub_subs['w'].send_message(
                {'type': 'roomCodeOk',
                 'code_type': room_code.code_type.value,
                 'room_name': self.handler.room.name})

        except KeyError:
            self.handler.send_malformed_message_error(
                message)

        except NoObjectReturnedFromDB:
            self.handler.send_error('codeNotPresentInDB',
                                    message,
                                    'This code is not '
                                    'present in the '
                                    'database.')
