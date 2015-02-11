import src


class CriticalLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'critical-panel'
    _class = 'scrolling-panel'
    conf = {
        'static_url_prefix': '/critical/',
        'static_path': './locking_panels/critical/static',
        'css_files': ['critical.css'],
        'js_files': [],
    }
    
    def render(self):
        return self.render_string(
            '../locking_panels/critical/critical.html')
