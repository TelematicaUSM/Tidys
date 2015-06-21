# -*- coding: UTF-8 -*-

from warnings import warn

from tornado.ioloop import IOLoop

from src import messages as msg

_path = msg.join_path('src', 'pub_sub')


class PubSub(object):

    """Implement the PubSub pattern.

    This class is designed to implement the PubSub pattern,
    in a way that is compatible with Tornado's coroutines.

    .. automethod:: __init__
    """

    _path = msg.join_path(_path, 'PubSub')

    def __init__(self, name='pub_sub_instance',
                 send_function=None):
        """Initialize the new PubSub object.

        :param str name:
            Name used to identify this object in debug
            messages.

        :param callable send_function:
            Function or coroutine to be called when sending
            a message. This function should not be called
            directly. When sending a message, call
            ``send_message`` instead of ``send_function``.
        """
        self.name = name
        self.send_function = send_function
        self.actions = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        """Return a string representation of the object."""
        t = '{0.__class__.__name__}' \
            "('{0.name}', {0.send_function.__qualname__})"
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

        :raises MsgIsNotDictError:
            If ``message`` is not a dictionary.

        :raises NoMessageTypeError:
            If ``message`` doesn't have the ``'type'`` key.

        :raises NoActionForMsgTypeError:
            If ``self.send_function`` wasn't specified
            during object creation and there's no
            registered action for this message type.
        """
        _path = msg.join_path(self._path, 'send_message')

        if not isinstance(message, dict):
            raise MsgIsNotDictError(message)

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

        :raises NoActionForMsgTypeError:
            If there's no registered action for this message
            type.

        :raises MsgIsNotDictError:
            If ``message`` is not an instance of ``dict``.
        """
        _path = msg.join_path(self._path, 'execute_actions')
        msg.code_debug(
            _path,
            'Message arrived: {}.'.format(message)
        )

        try:
            for action in self.actions[message['type']]:
                IOLoop.current().spawn_callback(action,
                                                message)
        except TypeError as te:
            if not isinstance(message, dict):
                raise MsgIsNotDictError(message) from te
            else:
                raise

        except KeyError as ke:
            if 'type' not in message:
                raise NoMessageTypeError(message) from ke

            elif message['type'] not in self.actions:
                nafmte = NoActionForMsgTypeError(message,
                                                 self.name)
                raise nafmte from ke
            else:
                raise

    def remove(self, msg_type, action):
        """Remove the action asociated with ``msg_type``.

        :param str msg_type:
            The message type that is asociated with
            ``action``.

        :param callable action:
            A function that was previously registered to
            ``msg_type``.

        :raises NoActionForMsgTypeError:
            If there's no registered action for this message
            type.
        """
        try:
            self.actions[msg_type].discard(action)

            if not self.actions[msg_type]:
                del self.actions[msg_type]

        except KeyError as ke:
            if msg_type not in self.actions:
                nafmte = NoActionForMsgTypeError(msg_type,
                                                 self.name)
                raise nafmte from ke
            else:
                raise


class OwnerPubSub(PubSub):
    # Used by inherited methods.
    _path = msg.join_path(_path, 'OwnerPubSub')

    def __init__(self, name='owner_pub_sub_instance',
                 send_function=None):
        super().__init__(name, send_function)
        self.owners = {}

    def register(self, msg_type, action, owner=None):
        super().register(msg_type, action)

        if owner in self.owners:
            self.owners[owner].add((msg_type, action))
        else:
            self.owners[owner] = {(msg_type, action)}

    def remove_owner(self, owner):
        """Remove all actions registered by ``owner``.

        :param object owner:
            Object that owns a set of actions registeres in
            this PubSub object.

        :raises UnrecognizedOwnerError:
            If ``owner`` wasn't previously registered in
            this PubSubobject.
        """
        try:
            for msg_type, action in self.owners[owner]:
                self.remove(msg_type, action)

            del self.owners[owner]

        except NoActionForMsgTypeError:
            warn(
                "This method tried to remove an action "
                "that was registered by an owner, but now "
                "isn't in ``self.actions``. This may be "
                "caused because two owners registered the "
                "same action. Please review your code. "
                "This may be a source of errors.")

        except KeyError as ke:
            if owner not in self.owners:
                uoe = UnrecognizedOwnerError(
                    'Owner {owner} is not registered in '
                    'the {ps.name} PubSub '
                    'object.'.format(owner=owner, ps=self)
                )
                raise uoe from ke
            else:
                raise


class MalformedMessageError(ValueError):

    """Raise when a message isn't in the expected format."""

    pass


class NoMessageTypeError(MalformedMessageError):

    """Rise when a message doesn't have the ``type`` key."""

    def __init__(self, *args):
        super().__init__(
            "All messages must have the 'type' key.", *args)


class UnrecognizedMessageError(KeyError):

    """Rise when a message type wasn't found in a dict."""

    pass


class NoActionForMsgTypeError(UnrecognizedMessageError):

    """Raise when there's no action for a message type."""

    def __init__(self, *args):
        super().__init__(
            "There's no registered action for this message "
            "type.",
            *args
        )


class UnrecognizedOwnerError(KeyError):

    """Rise when an owner wasn't found in a dict."""

    pass


class MsgIsNotDictError(TypeError):

    """Raise when a message is not an instance of dict."""

    def __init__(self, *args):
        super().__init__(
            'Messages must be instances of dict.',
            *args
        )
