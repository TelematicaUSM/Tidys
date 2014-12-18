from controller import app
from src.load import load_boiler_ui_modules
from logging import debug

load_boiler_ui_modules(__name__, app)
