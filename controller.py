# -*- coding: UTF-8 -*-

import json
from functools import partialmethod
from weakref import finalize

from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

import conf
from src import ui_modules, ui_methods, messages as msg
from src.boiler_ui_module import BoilerUIModule
from src.pub_sub import OwnerPubSub, NoMessageTypeError, \
    NoActionForMsgTypeError, MsgIsNotDictError

_path = 'controller'


class GUIHandler(RequestHandler):
    def get(self, _class):
        if _class:
            self.render('boxes.html',
                        classes={_class, 'system-panel'})
        else:
            self.render('boxes.html')


class MSGHandler(WebSocketHandler):

    """Serve the WebSocket clients.

    An instance of this class is created every time a
    client connects using WebSocket. The instances of this
    class deliver messages to a group of objects
    specialized in attending a group of messages.

    .. automethod:: _finalize
    """

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
        self.ws_objects = {
            ws_class: ws_class(self)
            for ws_class in self.ws_classes}

        # Call ``self._finalize`` when this object is about
        # to be destroyed.
        self.finalize = finalize(self, self._finalize)

        self.__class__.clients.add(self)
        self.__class__.client_count += 1

    @classmethod
    def add_class(cls, wsclass):
        cls.ws_classes.append(wsclass)

    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.ws_pub_sub.send_message(message)

    def on_message(self, message):
        """Process messages when they arrive.

        :param str message:
            The received message. This should be a valid
            json document.
        """
        try:
            # Throws ValueError
            message = json.loads(message)

            self.ws_pub_sub.execute_actions(message)

        except NoActionForMsgTypeError:
            self.send_error(
                'noActionForMsgType',
                message,
                "The client has sent a message for which "
                "there is no associated action."
            )
            msg.no_action_for_msg_type(_path, message)

        except (MsgIsNotDictError, NoMessageTypeError,
                ValueError):
            self.send_malformed_message_error(message)
            msg.malformed_message(_path, message)

    def send_error(self, critical_type, message,
                   description):
        self.ws_pub_sub.send_message(
            {'type': 'critical',
             'critical_type': critical_type,
             'message': message,
             'description': description}
        )

    send_malformed_message_error = partialmethod(
        send_error,
        'malformedMessage',
        description="The client has sent a message which "
                    "either isn't in JSON format, is not a "
                    "single JSON object, does not have a "
                    "'type' field or at least one "
                    "attribute is not consistent with the "
                    "others."
    )

    def _finalize(self):
        """Clean up the associated objects

        This method calls the ``unregister`` method of all
        objects in ``self.ws_objects`` and it removes
        ``self`` from ``self.__class__.clients``.

        This method should not be called directly.
        ``self.finalize`` is setup to call this method when
        the object is garbage collected, the WebSocket
        connection closes or when the program ends.
        To execute this method you should call
        ``self.finalize`` instead.
        """
        _path = msg.join_path(self._path, '_finalize')

        for ws_object in self.ws_objects.values():
            ws_object.unregister()

        self.__class__.clients.discard(self)

        msg.code_debug(
            _path,
            'Connection closed! {0} '
            '({0.request.remote_ip})'.format(self)
        )

    def on_close(self):
        self.finalize()


app = Application(
    [('/ws$', MSGHandler),
     ('/(.*)$', GUIHandler), ],
    debug=conf.debug,
    static_path='./static',
    template_path='./templates',
    ui_modules=[ui_modules],
    ui_methods=[ui_methods],
)

app.listen(conf.port)

# Import the modules which register actions in the
# MSGHandler
import locking_panels
import notifications
import panels

# BoilerUIModules that aren't automatically loaded from
# a package, must add their handlers to the app.
for module in app.ui_modules.values():
    if issubclass(module, BoilerUIModule):
        module.add_handler(app)
