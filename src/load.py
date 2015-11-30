import sys
from importlib import import_module
from inspect import isclass
from os.path import dirname
from pkgutil import iter_modules
from src import messages
from types import ModuleType

from .boiler_ui_module import BoilerUIModule
from .wsclass import WSClass


def get_module(module_name):
    """Return an instance of a module.

    If ``module_name`` is already an instance of a module,
    the module's instance is returned as is.

    :param module_name:
        A module name or a module instance.
    :type module_name: str or :class:`~types.ModuleType`
    """
    if isinstance(module_name, ModuleType):
        return module_name
    else:
        return sys.modules[module_name]


def load_python_modules(package):
    """Return a list of all the modules in ``package``.

    :param package:
        The package from which you want to get a list of all
        of its modules.
    :type package: str or :class:`~types.ModuleType`

    :return:
        A list containing the instances of all submodules of
        ``package``.
    :rtype: list of :class:`~types.ModuleType`
    """
    package = get_module(package)
    directory = dirname(package.__file__)
    modules = [import_module('.' + name, package.__name__)
               for _, name, _ in iter_modules([directory])]
    return modules


def load_boiler_ui_modules(package, app):
    """Register all BUIModules of ``package`` in ``app``.

    First, all the classes of type
    :class:`~src.boiler_ui_module.BoilerUIModule`, in all
    submodules of ``package``, are loaded and appended to a
    list called ``boiler_ui_modules``. The
    ``boiler_ui_modules`` list is created as an attribute of
    ``package``.

    After the list is created, the method
    :meth:`~src.boiler_ui_module.BoilerUIModule.add_handler`
    is called for all the
    :class:`~src.boiler_ui_module.BoilerUIModule` classes in
    the list. The call of this method registers a custom
    :class:`~tornado.web.StaticFileHandler` in the
    application.

    :param package:
        The package from which you want to register all of
        its :class:`~src.boiler_ui_module.BoilerUIModule`
        classes.
    :type package: str or :class:`~types.ModuleType`

    :param app:
        The Tornado application where all
        :class:`~src.boiler_ui_module.BoilerUIModule`
        classes will be registered.
    :type app: :class:`tornado.web.Application`
    """
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
    """Register all WSClasses of ``package`` in ``handler``.

    :param package:
        The package from which you want to register all of
        its :class:`~src.wsclass.WSClass` classes.
    :type package: str or :class:`~types.ModuleType`

    :param handler:
        The :class:`~controller.MSGHandler` where you want
        to register all :class:`~src.wsclass.WSClass`
        classes of ``package``.
    :type handler: :class:`~controller.MSGHandler`
    """
    package = get_module(package)
    python_modules = load_python_modules(package)

    for module in python_modules:
        for member in module.__dict__.values():
            if isclass(member) and \
               issubclass(member, WSClass):
                messages.code_debug(
                    'src.load.load_wsclasses',
                    'Adding WSClass {}.'.format(member)
                )
                handler.add_class(member)
