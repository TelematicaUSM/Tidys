import src


class LoadingLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'loading-panel'
    classes = {'scrolling-panel', 'system-panel'}
    conf = {
        'static_url_prefix': '/loading/',
        'static_path': './locking_panels/loading/static',
        'css_files': ['loading.css'],
        'js_files': [],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/loading/loading.html')
