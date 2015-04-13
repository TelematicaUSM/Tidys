# -*- coding: UTF-8 -*-

from sys import exit
from logging import info, debug, error, critical
from conf import app_name, port, proxy_url

def closing():
    info('%s: Closing ...', app_name)

def stopped():
    info('%s: Stopped!', app_name)

def starting():
    info('%s: Starting on port %d ...', app_name, port)

def wellcome():
    print(
        'Wellcome to %s! Open %s in your browser.' %
        (app_name, proxy_url)
    )

def code_related_message(code_path, message, print_f=print):
    print_f(
        '%s: %s' % (code_path, message)
    )

def code_info(code_path, message):
    code_related_message(code_path, message, print_f=info)

def code_debug(code_path, message):
    code_related_message(code_path, message, print_f=debug)

def code_error(code_path, message):
    code_related_message(code_path, message, print_f=error)

def code_critical(code_path, message):
    code_related_message(code_path, message,
                         print_f=critical)
    closing()
    exit()

def file_not_found(code_path, file_name, print_f=error):
    code_related_message(code_path,
        'file "%s" could not be found!'%file_name, print_f)

def unexpected_error(code_path):
    from sys import exc_info
    code_related_message(code_path,
        'Unexpected error: %s.'%exc_info()[0],
        print_f=error)

def duplicate_object_in_db(code_path, obj):
    code_error(code_path,
        'Unable to create duplicate object %r in the '
        'database!' % obj)

def try_new_id_after_dup_obj_in_db(code_path):
    code_info(code_path,
        'Trying to create a new object with a different id '
        '...')

def exhausted_tries(code_path):
    code_critical(code_path,
        'We exhausted all tries in an algorithm and '
        'didn\'t have luck. Try incrementing the maximum'
        'number of tries.')

def impossible_condition(code_path):
    code_critical(code_path,
                  'An impossible condition was met!')

def obj_creation_error(code_path, cls, *args, **kwargs):
    code_error(
        code_path,
        'Unable to create object from class %r, '
        'args=%r and kwargs=%r!' % (cls, args, kwargs)
    )
