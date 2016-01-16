import src


class HomeLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'home-panel'
    classes = {'scrolling-panel', 'system'}
    conf = {
        'static_url_prefix': '/home/',
        'static_path': './locking_panels/home/static',
        'css_files': ['home.css'],
        'js_files': [],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/home/home.html')
