from tornado.ioloop import IOLoop
from src import messages as msg
from src.db import message_broker as mb

_path = 'src.swclass'

class WSClass(object):
    _path = '.'.join((_path, 'WSClass'))

    def __init__(self, handler):
        _path = '.'.join((self._path, '__init__'))

        self.handler = handler
        self.action_registers = {
            'w': self.handler.register_action,
            'd': mb.register_action,
            'l': self.register_action,
        }

        for attr_name in dir(self):
            attribute = getattr(self, attr_name)
            if hasattr(attribute, 'msg_types'):
                for _type, channels in attribute.msg_types:
                    msg.code_debug(_path,
                        'Adding action: %r ...' % attribute)
######################################################


    def register_action_in(self, msg_type, action, channels,
                           owner=None):
        for channel in channels:
            register = self.action_registers[channel]

            if channel == 'w':
                register(owner, msg_type, action)
            else:
                register(msg_type, action)

    def register_action(self, msg_type, action):
        if msg_type in self._actions:
            self._actions[msg_type].add(action)
        else:
            self._actions[msg_type] = {action}

    def send_message(message):
        _path = '.'.join((self._path, 'send_message'))

        try:
            for action in self._actions[message['type']]:
                IOLoop.current().spawn_callback(action,
                                                message)
        except KeyError:
            if 'type' in message:
                msg.unrecognized_message_type(_path,
                                              message)
            else:
                msg.malformed_message(_path, message)

class subscribe(object):
    """Append the msg_types attribute to a method.

    Each parameter should in one of the following forms:
    type, (type, channel) or (type, {channel, ...}). Where
    type is a string containing the message_type to which
    you want the method to be subscribed and channel is one
    of this strings: 'w', 'd', 'l'. The channel strings
    mean: Websocket, Database and Local.
    
    This class should be used as a decorator.
    """

    _path = '.'.join((_path, 'subscribe'))

    def __init__(self, *msg_types, channels={'w','d','l'}):
        is_2_tuple = lambda t: isinstance(t, tuple) and \
                               len(t) == 2
        for t in msg_types:
            if not isinstance(t, (tuple,str)):
                raise TypeError

            elif not is_2_tuple(t):
                raise ValueError
            
        self.msg_types = [(t, channels)
                          for t in msg_types
                          if isinstance(t, str)]
        self.msg_types.extend(
            (t[0], {t[1]})
            if isinstance(t[1], str)
            else t
            for t in msg_types
            if is_2_tuple(t)
        )

    def __call__(self, method):
        _path = '.'.join((self._path, '__call__'))
        msg.code_debug(
            _path,
            'Subscribing method {!r} to {!r} message types '
            '...'.format(method, self.msg_types)
        )
        method.msg_types = self.msg_types
        return method
