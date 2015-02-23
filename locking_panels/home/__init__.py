import src


class HomeLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'home-panel'
    _class = 'scrolling-panel'
    conf = {
        'static_url_prefix': '/home/',
        'static_path': './locking_panels/home/static',
        'css_files': ['home.css'],
        'js_files': [],
    }
    
    def render(self):
        return self.render_string(
            '../locking_panels/home/home.html')
