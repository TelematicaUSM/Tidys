# -*- coding: UTF-8 -*-

from logging import info
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

def file_not_found(print_f, function_name, file_name):
    print_f(
        '%s: file "%s" could not be found!' %
        (function_name, file_name)
    )
