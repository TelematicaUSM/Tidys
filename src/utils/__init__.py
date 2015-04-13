# -*- coding: UTF-8 -*-

from string import ascii_letters, digits, punctuation
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import coroutine

def random_word(length,
                charset=ascii_letters+digits+punctuation):
    from random import choice
    return ''.join(
        choice(charset)
        for i in range(length)
    )

class run_inside(object):
    def __init__(self, outher_function):
        self.outher_function = outher_function
    
    def __call__(self, inner_function):
        from functools import update_wrapper
    
        def run(*args, **kwargs):
            return self.outher_function(
                lambda: inner_function(*args, **kwargs)
            )
            
        update_wrapper(run, inner_function)
        return run

class always_run_in_thread(object):
    def __init__(self, func):
        self.func = func
    
    @coroutine
    def __call__(self, *args, **kwargs):
        with ThreadPoolExecutor(1) as thread:
            result = yield thread.submit(self.func, *args,
                                         **kwargs)
        return result

@coroutine
def run_in_thread(func, *args, **kwargs):
    with ThreadPoolExecutor(1) as thread:
        result = yield thread.submit(func, *args, **kwargs)
    return result
