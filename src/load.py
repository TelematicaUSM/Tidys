from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules
from types import ModuleType
from .boiler_ui_module import BoilerUIModule

def load_python_modules(package):
    directory = dirname(package.__file__)
    modules = [import_module('.' + name, package.__name__)
               for _, name, _ in iter_modules([directory])]
    return modules

def load_boiler_ui_modules(package, app):
    python_modules = load_python_modules(package)
    package.boiler_ui_modules = [member
        for module in python_modules
        for member in module.__dict__.values()
        if issubclass(member, BoilerUIModule)]
    
    for module in package.boiler_ui_modules:
        module.add_handler(app)
