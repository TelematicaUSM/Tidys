import src


class LoadingLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'loading-panel'
    _class = 'scrolling-panel'
    conf = {
        'static_url_prefix': '/loading/',
        'static_path': './locking_panels/loading/static',
        'css_files': ['loading.css'],
        'js_files': [],
    }
    
    def render(self):
        return self.render_string(
            '../locking_panels/loading/loading.html')
