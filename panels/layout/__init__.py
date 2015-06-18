import src


class Layout(src.boiler_ui_module.BoilerUIModule):
    id_ = 'layout'
    classes = {'fixed-panel'}
    name = 'Layout'
    conf = {
        'static_url_prefix': '/layout/',
        'static_path': './panels/layout/static',
        'css_files': ['layout.css'],
        'js_files': [],
    }

    def render(self):
        return self.render_string(
            '../panels/layout/layout.html')
