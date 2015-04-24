from controller import app, MSGHandler
from src.load import load_boiler_ui_modules

load_boiler_ui_modules(__name__, app)
