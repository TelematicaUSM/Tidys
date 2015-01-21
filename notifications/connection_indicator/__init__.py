import src


class UI(src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/conn-ind/',
        'static_path': './notifications/'
                       'connection_indicator/static',
        'css_files': ['style.css'],
        'js_files': ['script.js'],
    }
    
    def render(self):
        return self.render_string(
            '../notifications/connection_indicator/UI.html')
