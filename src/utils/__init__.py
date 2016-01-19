# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from string import ascii_letters, digits, punctuation
from concurrent.futures import ThreadPoolExecutor

from tornado.gen import coroutine


def random_word(
        length,
        charset=ascii_letters + digits + punctuation):
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


def all_attr_defined(obj, *attributes):
    return all(hasattr(obj, a) and
               getattr(obj, a) is not None
               for a in attributes)


def raise_if_all_attr_def(obj, *attributes):
    from src.messages import code_debug

    if all_attr_defined(obj, *attributes):
        raise
    else:
        code_debug(
            'src.utils.raise_if_all_attr_def',
            'An exception was suppressed. '
            '{}, {}.'.format(obj, attributes)
        )


def standard_name(name):
    """Standardise a name string.

    This function transforms a string, eliminating white
    space, normalizing it and case folding it. This makes it
    possible to use the string as an identifier, preventing
    the use of similar string keys at the same time.

    :param str name:
        A name to be standardised.

    :return:
        The standard version of `name`.
    :rtype: str

    :raises TypeError:
        If ``name`` is not a string.
    """
    from collections import Iterable, Callable
    from unicodedata import normalize

    try:
        splitted = name.split()
        compacted = ''.join(splitted)
        normalized = normalize('NFKC', compacted)
        return normalized.casefold()

    except (AttributeError, TypeError) as e:
        if not hasattr(name, 'split') or \
                not isinstance(name.split, Callable) or \
                not isinstance(splitted, Iterable) or \
                not all(
                    isinstance(e, str) for e in splitted):
            te = TypeError(
                "The name parameter doesn't seem to be a "
                "string.")
            raise te from e

        else:
            raise
