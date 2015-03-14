# -*- coding: UTF-8 -*-

def random_word(length):
    from random import choice
    from string import ascii_letters, digits, punctuation
    return ''.join(
        choice(ascii_letters+digits+punctuation)
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
