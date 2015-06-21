# -*- coding: UTF-8 -*-

from functools import partialmethod
from weakref import finalize

from src import messages as msg
from src.db import message_broker as mb
from src.pub_sub import MalformedMessageError, \
    UnrecognizedOwnerError

_path = 'src.swclass'


class WSClass(object):

    """Attaches its methods to a controller.MSGHandler.

    .. todo::
        *   Explain this class better XD.
    """

    _path = '.'.join((_path, 'WSClass'))

    def __init__(self, handler):
        _path = msg.join_path(self._path, '__init__')

        self.handler = handler
        self.pub_subs = {
            'w': self.handler.ws_pub_sub,
            'd': mb,
            'l': self.handler.local_pub_sub,
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
                        channels=channels)

        finalize(
            self, msg.code_debug, self._path,
            'Deleting WSClass {0} from {0.handler} '
            '...'.format(self)
        )

    @property
    def channels(self):
        return self.pub_subs.keys()

    def redirect_to(self, channel, message, content=False):
        """Redirect ``message`` through ``channel``.

        If ``content`` is ``True``, then the the object
        corresponding to the ``'content'`` key of
        ``message`` is sent.

        :param str channel:
            The channel through which ``message`` will be
            sent.

        :param dict message:
            The message to be sent.

        :param bool content:
            If ``True``, the whole message will be sent.
            If ``False``, just the object corresponding to
            the ``'content'`` key of ``message`` will be
            sent.

        :raises MalformedMessageError:
            If ``content`` is ``True``, but ``message``
            doesn't have the ``'content'`` key.

        :raises BadChannelArgumentError:
            If ``channel`` is not one of ``self.pub_subs``
            keys.

        :raises MsgIsNotDictError:
            If ``message`` is not a dictionary.

        :raises NoMessageTypeError:
            If the message or it's content doesn't have the
            ``'type'`` key.

        :raises NoActionForMsgTypeError:
            If ``send_function`` of the ``PubSub`` object
            wasn't specified during object creation and
            there's no registered action for this message
            type.
        """
        try:
            m = message['content'] if content else message
            self.pub_subs[channel].send_message(m)

        except KeyError as ke:
            if 'content' not in message:
                mme = MalformedMessageError(
                    "If content=True, then message must "
                    "have the 'content' key."
                )
                raise mme from ke

            elif channel not in self.pub_subs:
                raise \
                    BadChannelArgumentError(self.channels) \
                    from ke
            else:
                raise

    redirect_content_to = partialmethod(redirect_to,
                                        content=True)

    def register_action_in(self, msg_type, action,
                           channels):
        """Register ``action`` in a set of channels.

        :param str msg_type:
            The message type to which ``action`` will be
            subscribed.

        :param callable action:
            The action to be registered in ``channels``.

        :param set channels:
            Set of strings, which identify all the channels
            to which ``action`` will be registered.

        :raises BadChannelArgumentError:
            If any channel is not one of ``self.pub_subs``
            keys.
        """
        try:
            for channel in channels:
                ps = self.pub_subs[channel]
                ps.register(msg_type, action, self)

        except KeyError as ke:
            if not all(c in self.pub_subs
                       for c in channels):
                raise \
                    BadChannelArgumentError(self.channels) \
                    from ke
            else:
                raise

    def unregister(self):
        for ps in self.pub_subs.values():
            try:
                ps.remove_owner(self)
            except UnrecognizedOwnerError:
                pass


class subscribe(object):

    """Append the ``msg_types`` attribute to a method.

    Each parameter should have one of the following forms:
    ``type``, ``(type, channel)`` or
    ``(type, {channel, ...})``. Where ``type`` is a string
    containing the message_type to which you want the method
    to be subscribed and ``channel`` is one of this strings:
    ``'w'``, ``'d'``, ``'l'``. The channel strings mean:
    Websocket, Database and Local.

    This class should be used as a decorator.

    :raises TypeError:
        If any element of ``msg_types`` is not a tuple or a
        string.

    :raises ValueError:
        If any tuple in ``msg_types`` has a length different
        than 2.
    """

    _path = '.'.join((_path, 'subscribe'))

    def __init__(self, *msg_types,
                 channels={'w', 'd', 'l'}):

        for t in msg_types:
            if not isinstance(t, (tuple, str)):
                raise TypeError(
                    'msg_types has an element that is not '
                    'a tuple or a string.'
                )

            if isinstance(t, tuple) and len(t) != 2:
                raise ValueError(
                    'msg_types has a tuple that has a '
                    'length different than 2.'
                )

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


class BadChannelArgumentError(ValueError):
    def __init__(channels, *args):
        super().__init__(
            'The channel argument must be one of the '
            'following strings: {}.'.format(channels),
            *args
        )
