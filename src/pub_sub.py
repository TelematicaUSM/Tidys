# -*- coding: UTF-8 -*-

from tornado.ioloop import IOLoop

from src import messages as msg

_path = msg.join_path('src', 'pub_sub')


class PubSub(object):

    """Implement the PubSub pattern.

    This class is designed to implement the PubSub pattern,
    in a way that is compatible with Tornado's coroutines.

    .. automethod:: __init__
    .. automethod:: __str__
    .. automethod:: __repr__
    """

    _path = msg.join_path(_path, 'PubSub')

    def __init__(self, send_function=None,
                 name='pub_sub_instance'):
        """Initialize the new PubSub object.

        :param callable send_function:
            Function or coroutine to be called when sending
            a message. This function should not be called
            directly. When sending a message, call
            ``send_message`` instead of ``send_function``.

        :param str name:
            Name used to identify this object in debug
            messages.

        .. todo::
            *   Invert the order of the ``send_function``
                and ``name`` attributes.
        """
        self.send_function = send_function
        self.name = name
        self.actions = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        """Return a string representation of the object.

        .. todo::
            *   Invert the order of the ``send_function``
                and ``name`` attributes.
        """
        t = '{0.__class__.__name__}' \
            "({0.send_function}, '{0.name}')"
        return t.format(self)

    def register(self, msg_type, action):
        if msg_type in self.actions:
            self.actions[msg_type].add(action)
        else:
            self.actions[msg_type] = {action}

    def send_message(self, message):
        """Send a message

        ``self.send_function`` is used if it was specified
        during object creation. If not,
        ``self.execute_actions`` is used.

        :param dict message: The message to be sent.

        :raises TypeError:
            If ``message`` is not a dictionary.

        :raises NoMessageTypeError:
            If ``message`` doesn't have the ``'type'`` key.

        :raises UnrecognizedMessageError:
            If ``self.send_function`` wasn't specified
            during object creation and there's no
            registered action for this message type.
        """
        _path = msg.join_path(self._path, 'send_message')

        if not isinstance(message, dict):
            raise TypeError(
                'The message argument must be a '
                'dictionary.',
                message
            )

        if 'type' not in message:
            raise NoMessageTypeError(message)

        msg.code_debug(
            _path,
            'Sending message: {}.'.format(message)
        )

        if self.send_function is None:
            self.execute_actions(message)
        else:
            IOLoop.current().spawn_callback(
                self.send_function, message)

    def execute_actions(self, message):
        """Execute actions associated to the type of message

        :param dict message: The message to be sent

        :raises NoMessageTypeError:
            If ``message`` doesn't have the ``'type'`` key.

        :raises UnrecognizedMessageError:
            If there's no registered action for this message
            type.

        .. todo::
            *   Handle TypeError when ``message`` is not a
                ``dict``.
        """
        try:
            for action in self.actions[message['type']]:
                IOLoop.current().spawn_callback(action,
                                                message)
        except KeyError as ke:
            if 'type' not in message:
                raise NoMessageTypeError(message) from ke

            elif message['type'] not in self.actions:
                ume = UnrecognizedMessageError(
                    "There's no registered action for "
                    "this message type.",
                    message
                )
                raise ume from ke

            else:
                raise

    def remove(self, msg_type, action):
        self.actions[msg_type].discard(action)

        if not self.actions[msg_type]:
            del self.actions[msg_type]


class OwnerPubSub(PubSub):
    # Used by inherited methods.
    _path = msg.join_path(_path, 'OwnerPubSub')

    def __init__(self, send_function=None,
                 name='owner_pub_sub_instance'):
        super().__init__(send_function, name)
        self.owners = {}

    def register(self, msg_type, action, owner=None):
        super().register(msg_type, action)

        if owner in self.owners:
            self.owners[owner].add((msg_type, action))
        else:
            self.owners[owner] = {(msg_type, action)}

    def remove_owner(self, owner):
        for msg_type, action in self.owners[owner]:
            self.remove(msg_type, action)

        del self.owners[owner]


class MalformedMessageError(ValueError):
    pass


class NoMessageTypeError(MalformedMessageError):
    def __init__(*args):
        super().__init__(
            "All messages must have the 'type' key.", *args)


class UnrecognizedMessageError(Exception):
    pass
