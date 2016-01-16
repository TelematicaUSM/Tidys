import src


class RemotePanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'remote-panel'
    classes = {'scrolling-panel', 'teacher'}
    name = 'Control Remoto'
    conf = {
        'static_url_prefix': '/remote/',
        'static_path': './panels/remote/static',
        'css_files': ['remote.css'],
        'js_files': ['remote.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/remote/remote.html')
