import src


class CriticalLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'critical-panel'
    classes = {'scrolling-panel', 'system-panel'}
    conf = {
        'static_url_prefix': '/critical/',
        'static_path': './locking_panels/critical/static',
        'css_files': ['critical.css'],
        'js_files': [],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/critical/critical.html')
