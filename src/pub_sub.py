# -*- coding: UTF-8 -*-

from tornado.ioloop import IOLoop

from src import messages as msg

_path = 'src.pub_sub'


class PubSub(object):
    _path = msg.join_path(_path, 'PubSub')

    def __init__(self):
        self.actions = {}

    def register(self, msg_type, action):
        if msg_type in self.actions:
            self.actions[msg_type].add(action)
        else:
            self.actions[msg_type] = {action}

    def distribute_message(self, message):
        _path = msg.join_path(self._path,
                              'distribute_message')

        try:
            for action in self.actions[message['type']]:
                IOLoop.current().spawn_callback(action,
                                                message)
        except KeyError:
            if 'type' in message:
                msg.unrecognized_message_type(_path,
                                              message)
            else:
                msg.malformed_message(_path, message)

    def remove(self, msg_type, action):
        self.actions[msg_type].discard(action)

        if not self.actions[msg_type]:
            del self.actions[msg_type]


class OwnerPubSub(PubSub):
    def __init__(self):
        super().__init__()
        self.owners = {}

    def register(self, msg_type, action, owner=None):
        super().register(msg_type, action)

        if owner in self.owners:
            self.owners[owner].add((msg_type, action))
        else:
            self.owners[owner] = {(msg_type, action)}

        # FIXME
        from termcolor import cprint
        l = len(self.owners)
        cprint('Actual message owners: {}'.format(l), 'red')

    def remove_owner(self, owner):
        for msg_type, action in self.owners[owner]:
            self.remove(msg_type, action)

        del self.owners[owner]

        # FIXME
        from termcolor import cprint
        l = len(self.owners)
        cprint('Actual message owners: {}'.format(l), 'red')
