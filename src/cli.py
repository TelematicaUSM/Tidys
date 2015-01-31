# -*- coding: UTF-8 -*-

"""Provides a simple command line interface."""

import readline

from sys import modules
from src import messages


commands = {
    'help': {
        'desc': 'Shows this help message.',
        'syns': ('help', 'h', )},
    'close': {
        'desc': 'Closes the application.',
        'syns': ('close', 'q', 'quit', 'exit', 'stop', )},
}

def start():
    messages.wellcome()

    while True:
        i = input('>>> ')
        
        if not i:
            pass
        elif i in commands['close']['syns']:
            messages.closing()
            return
        elif i in commands['help']['syns']:
            help(modules[__name__])
        else:
            try:
                exec(i)
            except (SyntaxError, NameError):
                print('Error!')
