# -*- coding: UTF-8 -*-

"""Provides a simple command line interface."""

import readline

from sys import modules
from logging import info
from controller import MSGHandler
from conf import app_name


commands = {
    'help': {
        'desc': 'Shows this help message.',
        'syns': ('help', 'h', )},
    'close': {
        'desc': 'Closes the application.',
        'syns': ('close', 'q', 'quit', 'exit', 'stop', )},
}

def start():
    print('Type h for help or any python command.')

    while True:
        i = input('>>> ')
        
        if not i:
            pass
        elif i in commands['close']['syns']:
            info('%s: Closing ...', app_name)
            return
        elif i in commands['help']['syns']:
            help(modules[__name__])
        else:
            try:
                exec(i)
            except (SyntaxError, NameError):
                print('Error!')

def clients():
    total = MSGHandler.client_count
    current = len(MSGHandler.clients)
    print('Connected clients: %d' % current)
    print('Total connections opened: %d' % total)
    print('Total connections closed: %d' % (total-current))

def bcast(message):
    MSGHandler.broadcast(message)
