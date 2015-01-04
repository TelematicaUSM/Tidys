from controller import app, MSGHandler
from src.load import load_boiler_ui_modules, load_wsclasses
from logging import debug

load_boiler_ui_modules(__name__, app)
load_wsclasses(__name__, MSGHandler)
