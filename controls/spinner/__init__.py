import src


class SpinnerControl(src.boiler_ui_module.BoilerUIModule):
    conf = {
        'static_url_prefix': '/spinner/',
        'static_path': './controls/spinner/static',
        'css_files': ['spinner.css'],
        'js_files': [],
    }

    def render(self, id_=None):
        return self.render_string(
            '../controls/spinner/spinner.html',
            id_=id_)
