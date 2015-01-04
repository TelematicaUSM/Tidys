import sys

from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules
from inspect import isclass
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
    package.boiler_ui_modules = [member
        for module in python_modules
        for member in module.__dict__.values()
        if isclass(member)
        if issubclass(member, BoilerUIModule)]
    
    for module in package.boiler_ui_modules:
        module.add_handler(app)

def load_wsclasses(package, handler):
    package = get_module(package)
    python_modules = load_python_modules(package)
    
    for module in python_modules:
        for member in module.__dict__.values():
            if isclass(member) and issubclass(member,
                                              WSClass):
                handler.add_class(member)
