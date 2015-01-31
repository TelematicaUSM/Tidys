# -*- coding: UTF-8 -*-

from logging import info
from conf import app_name, port, expected_scheme, \
                 expected_host

def closing():
    info('%s: Closing ...', app_name)

def starting():
    info('%s: Starting on port %d ...', app_name, port)

def wellcome():
    print(
        'Wellcome to %s! Open %s://%s:%d in your browser.' %
        (app_name, expected_scheme, expected_host, port)
    )
    print('Type h for help or any python command.')
