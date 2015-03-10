# -*- coding: UTF-8 -*-

from logging import info, debug, error
from conf import app_name, port, proxy_scheme, proxy_host, \
                 proxy_port

def closing():
    info('%s: Closing ...', app_name)

def stopped():
    info('%s: Stopped!', app_name)

def starting():
    info('%s: Starting on port %d ...', app_name, port)

def wellcome():
    print(
        'Wellcome to %s! Open %s://%s%s in your browser.' %
        (app_name, proxy_scheme, proxy_host,
         ':%d'%proxy_port if proxy_port else '')
    )

def code_related_message(code_path, message, print_f=print):
    print_f(
        '%s: %s' % (code_path, message)
    )

def code_debug(code_path, message):
    code_related_message(code_path, message, print_f=debug)

def file_not_found(code_path, file_name, print_f=error):
    code_related_message(code_path,
        'file "%s" could not be found!'%file_name, print_f)

def unexpected_error(code_path):
    from sys import exc_info
    code_related_message(code_path,
        'Unexpected error: %s.'%exc_info()[0],
        print_f=error)
