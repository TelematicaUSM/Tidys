from src import messages as msg
from src.db import message_broker as mb

_path = 'src.swclass'


class WSClass(object):
    _path = '.'.join((_path, 'WSClass'))

    def __init__(self, handler):
        _path = '.'.join((self._path, '__init__'))

        self.handler = handler
        self._action_registers = {
            'w': self.handler.register_action,
            'd': mb.register_action,
            'l': self.handler.local_register_action,
        }

        for attr_name in dir(self):
            attribute = getattr(self, attr_name)
            if hasattr(attribute, 'msg_types'):
                for _type, channels in attribute.msg_types:
                    msg.code_debug(
                        _path,
                        'Adding action: %r ...' % attribute
                    )
                    self.register_action_in(
                        msg_type=_type, action=attribute,
                        channels=channels, owner=self)

    def __del__(self):
        _path = '.'.join((self._path, '__del__'))
        msg.code_debug(_path, 'Deleting WSClass ...')

        mb.remove_owner(self)

    def register_action_in(self, msg_type, action, channels,
                           owner=None):
        for channel in channels:
            register = self._action_registers[channel]

            if channel == 'd':
                register(owner, msg_type, action)
            else:
                register(msg_type, action)


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

    def __init__(self, *msg_types,
                 channels={'w', 'd', 'l'}):

        for t in msg_types:
            if not isinstance(t, (tuple, str)):
                raise TypeError

            if isinstance(t, tuple) and len(t) != 2:
                raise ValueError

        self.msg_types = [(t, channels)
                          for t in msg_types
                          if isinstance(t, str)]
        self.msg_types.extend(
            (t[0], {t[1]})
            if isinstance(t[1], str)
            else t
            for t in msg_types
            if isinstance(t, tuple)
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
