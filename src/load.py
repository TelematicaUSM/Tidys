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


import sys

from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules
from inspect import isclass
from src import messages
from .boiler_ui_module import BoilerUIModule
from . wsclass import WSClass


def get_module(module_name):
    if isinstance(module_name, str):
        return sys.modules[module_name]
    else:
        return module_name


def load_python_modules(package):
    package = get_module(package)
    directory = dirname(package.__file__)
    modules = [import_module('.' + name, package.__name__)
               for _, name, _ in iter_modules([directory])]
    return modules


def load_boiler_ui_modules(package, app):
    package = get_module(package)
    python_modules = load_python_modules(package)
    package.boiler_ui_modules = [
        member
        for module in python_modules
        for member in module.__dict__.values()
        if isclass(member)
        if issubclass(member, BoilerUIModule)
    ]

    for module in package.boiler_ui_modules:
        module.add_handler(app)


def load_wsclasses(package, handler):
    package = get_module(package)
    python_modules = load_python_modules(package)

    for module in python_modules:
        for member in module.__dict__.values():
            if isclass(member) and issubclass(member,
                                              WSClass):
                messages.code_debug(
                    'src.load.load_wsclasses',
                    'Adding WSClass {}.'.format(member)
                )
                handler.add_class(member)
