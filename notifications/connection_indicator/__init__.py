import src


class ConnectionIndicator(
        src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/conn-ind/',
        'static_path': './notifications/'
                       'connection_indicator/static',
        'css_files': ['conn-ind.css'],
        'js_files': ['conn-ind.js'],
    }
    
    def render(self):
        return self.render_string(
            '../notifications/connection_indicator/'
            'conn-ind.html')
