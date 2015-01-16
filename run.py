# -*- coding: UTF-8 -*-

import readline

from threading import Thread
from logging import info
from tornado.ioloop import IOLoop
from conf import app_name, port
from controller import app

commands = {
    'help': {
        'desc': 'Shows this help message.',
        'syns': ('help', 'h', )},
    'close': {
        'desc': 'Closes the application.',
        'syns': ('close', 'q', 'quit', 'exit', 'stop', )},
}

def print_help():
    print('\nHelp:')
    for name, data in commands.items():
        print(
            '\t%s: %s\n\t\tSynonyms: %s.\n' % (
                name,
                data['desc'],
                ', '.join(data['syns'])
            )
        )

info('%s: Starting on port %d ...', app_name, port)
app.listen(port)

ioloop = IOLoop.instance()
t = Thread(target=lambda:ioloop.start())
t.start()

print_help()

while True:
    i = input('$ ')
    if i in commands['close']['syns']:
        info('%s: Closing ...', app_name)
        break
    elif i in commands['help']['syns']:
        print_help()
    else:
        print("'%s' is not a command." % i)

ioloop.add_callback(lambda:ioloop.stop())
t.join()
