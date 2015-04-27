import src


class SpinnerControl(src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/spinner/',
        'static_path': './controls/spinner/static',
        'css_files': ['spinner.css'],
        'js_files': [],
    }
    
    def render(self, _id=None):
        return self.render_string(
            '../controls/spinner/spinner.html',
            _id=_id)
