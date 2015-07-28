# -*- coding: UTF-8 -*-

"""Render the user panel and process all user messages.

This module patches the :class:`controller.MSGHandler`
class, adding the
:meth:`controller.MSGHandler.send_user_not_loaded_error`,
:meth:`controller.MSGHandler.send_room_not_loaded_error` and
:meth:`controller.MSGHandler.logout_and_close` methods.
"""

from functools import partialmethod

import jwt
from tornado.gen import coroutine
from pymongo.errors import OperationFailure

import src
from controller import MSGHandler
from backend_modules import router
from src import messages as msg
from src.db import User, Code, NoObjectReturnedFromDB, \
    ConditionNotMetError, CodeType, Course
from src.wsclass import subscribe
from src.pub_sub import MalformedMessageError
from src.utils import raise_if_all_attr_def

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


def _logout_and_close(self, reason):
    """Send a logout message and close the connection."""
    self.write_message({'type': 'logout'})
    self.close(1000, reason)
    self.clean_closed = True
MSGHandler.logout_and_close = _logout_and_close


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

    def __init__(self, handler):
        super().__init__(handler)
        self.session_start_ok = False

    @coroutine
    def load_user(self, token):
        try:
            uid = jwt.decode(token, verify=False)['id']
            user = yield User(uid)
            jwt.decode(token, user.secret)
            self.handler.user = user

        except NoObjectReturnedFromDB as norfdb:
            ite = jwt.InvalidTokenError(
                'No user was found in the database for '
                'this token.'
            )
            raise ite from norfdb

    @subscribe('logout', channels={'l'})
    def logout(self, message):
        try:
            blocked = \
                hasattr(self.handler, 'block_logout') and \
                self.handler.block_logout

            if blocked:
                self.handler.block_logout = False
            else:
                self.handler.logout_and_close(
                    message['reason'])

        except KeyError as ke:
            if 'reason' not in message:
                mme = MalformedMessageError(
                    "'reason' key not found in message.")
                raise mme from ke
            else:
                raise

    @subscribe('userMessage', channels={'w', 'l'})
    def send_user_message(self, message):
        """Send a message to all instances of a single user.

        The user id is appended to the message type and
        ``message`` is sent through the database.
        """
        try:
            message['type'] = '{}({})'.format(
                message['type'], self.handler.user.id)

            self.redirect_to('d', message)

        except MalformedMessageError:
            self.handler.send_malformed_message_error(
                message)
            msg.malformed_message(_path, message)

        except AttributeError:
            if not hasattr(self.handler, 'user'):
                self.send_user_not_loaded_error(message)
            else:
                raise

    def sub_to_user_messages(self):
        """Route messages of the same user to the local PS.

        This method subscribes
        :meth:`backend_modules.router.RouterWSC.to_local` to
        the messages of type ``userMessage(uid)`` coming
        from the database pub-sub. Where ``uid`` is the
        current user id.

        After the execution of this method,
        ``self.handler.user_msg_type`` contains the message
        type to be used to send messages to all instances of
        the user.
        """
        self.handler.user_msg_type = \
            'userMessage({})'.format(self.handler.user.id)

        router_object = self.handler.ws_objects[
            router.RouterWSC]
        self.register_action_in(
            self.handler.user_msg_type,
            action=router_object.to_local,
            channels={'d'}
        )

    def send_session_start_error(self, message, causes):
        """Send a session error message to the client.

        :param dict message:
            The message that caused the error.

        :param str causes:
            A string explaining the posible causes of the
            error.
        """
        try:
            self.handler.send_error(
                'session.start.error',
                message,
                'La sesión no se ha podido iniciar. ' +
                causes
            )

        except TypeError as e:
            if not isinstance(message, dict):
                te = TypeError(
                    'message should be a dictionary.')
                raise te from e

            elif not isinstance(causes, str):
                te = TypeError(
                    'causes should be a string.')
                raise te from e

            else:
                raise

    @coroutine
    def load_room_code(self, room_code_str):
        if room_code_str == 'none':
            self.handler.room_code = None
            self.handler.room = None
            code_type = 'none'
            room_name = None
        else:
            self.handler.room_code = \
                yield Code(room_code_str)
            self.handler.room = \
                yield self.handler.room_code.room

            code_type = \
                self.handler.room_code.code_type.name
            room_name = self.handler.room.name

        return (code_type, room_name)

    def redirect_to_teacher_view(self, room_code, message):
        """Redirect the client to the current teacher view.

        .. todo:
            *   Use send_session_start_error instead of
                handler.send_error.
        """
        if room_code == 'none':
            err_msg = "Can't redirect user to the " \
                "teacher view. This can be caused by an " \
                "inconsistency in the database."

            self.handler.send_error(
                'databaseInconsistency', message, err_msg)

            raise Exception(err_msg)

        self.pub_subs['w'].send_message(
            {
                'type': 'replaceLocation',
                'url': room_code
            }
        )

    @subscribe('session.start', 'w')
    @coroutine
    def startSession(self, message):
        try:
            yield self.load_user(message['token'])
            self.sub_to_user_messages()
            code_type, room_name = \
                yield self.load_room_code(
                    message['room_code'])

            distinct_room = \
                room_name is not None \
                and \
                self.handler.user.room_name is not None \
                and \
                room_name != self.handler.user.room_name

            was_none = self.handler.user.status == 'none'
            was_student = self.handler.user.status == 'seat'
            was_teacher = self.handler.user.status == 'room'

            is_none = code_type == 'none'
            is_student = code_type == 'seat'
            is_teacher = code_type == 'room'

            if distinct_room or was_student or \
                    is_student or (was_none and is_teacher):
                self.handler.block_logout = True
                self.pub_subs['d'].send_message(
                    {
                        'type': self.handler.user_msg_type,
                        'content': {
                            'type': 'logout',
                            'reason': 'exclusiveLogin'
                        }
                    }
                )

            course_id = self.handler.user.course_id

            if was_teacher:
                if is_none:
                    self.redirect_to_teacher_view(
                        self.handler.user.room_code,
                        message
                    )
                    # The rest of the code is not executed.
                    return

                elif course_id is not None:
                    if is_teacher:
                        self.handler.course = \
                            yield Course(course_id)

                    elif is_student:
                        yield \
                            self.handler.room.\
                            deassign_course(course_id)

                        yield self.handler.user.reset(
                            'course_id')

            yield self.handler.user.store_dict(
                {
                    'room_name': room_name,
                    'room_code': message['room_code'],
                    'status': code_type,
                }
            )

            if is_student:
                yield self.handler.room.use_seat(
                    self.handler.room_code.seat_id)

            yield self.handler.user.increase_instances()
            self.session_start_ok = True

            self.pub_subs['w'].send_message(
                {
                    'type': 'session.start.ok',
                    'code_type': code_type,
                    'course_id': course_id
                }
            )

        except jwt.InvalidTokenError:
            self.handler.logout_and_close('invalidToken')

        except ConditionNotMetError:
            self.send_session_start_error(
                message,
                'Es probable que este error se daba a que '
                'el asiento que desea registrar ya está '
                'usado.'
            )

        except OperationFailure:
            self.send_session_start_error(
                message,
                'Una operación de la base de datos ha '
                'fallado.'
            )

        except KeyError:
            keys_in_message = all(
                map(
                    lambda k: k in message,
                    ('token', 'room_code')
                )
            )
            if not keys_in_message:
                self.handler.send_malformed_message_error(
                    message)
            else:
                raise

    @subscribe('getUserName', 'w')
    def get_user_name(self, message):
        """Send the user's name to the client.

        .. todo::
            *   Re-raise attribute error and review error
                handling.
        """
        try:
            name = self.handler.user.name
            self.pub_subs['w'].send_message(
                {'type': 'userName',
                 'name': name})
        except AttributeError:
            self.send_user_not_loaded_error(message)

    @coroutine
    def end(self):
        yield super().end()

        try:
            if self.session_start_ok:
                yield self.handler.user.decrease_instances()
        except:
            raise_if_all_attr_def(self.handler, 'user')

        try:
            if self.handler.room_code.code_type is \
                    CodeType.room and \
                    self.handler.user.instances == 0:
                yield self.handler.room.deassign_course(
                    self.handler.course.id)
        except:
            raise_if_all_attr_def(
                self.handler, 'room_code', 'user', 'room',
                'course')

        try:
            if self.handler.room_code.code_type is \
                    CodeType.seat:
                yield self.handler.room.leave_seat(
                    self.handler.room_code.seat_id)
        except:
            raise_if_all_attr_def(
                self.handler, 'room_code', 'room')
