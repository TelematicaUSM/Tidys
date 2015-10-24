import src


class DontUnderstandIndicator(
        src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/dont_understand/',
        'static_path': './notifications/'
                       'dont_understand/static',
        'css_files': ['dont_understand.css'],
        'js_files': ['dont_understand.js'],
    }

    def render(self):
        return self.render_string(
            '../notifications/dont_understand/'
            'dont_understand.html')
