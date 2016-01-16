import src

class PresentationPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'presentation-panel'
    classes = {'fixed-panel', 'teacher'}
    name = 'Panel de Presentacion'
    conf = {
        'static_url_prefix': '/presentation/',
        'static_path': './panels/presentation/static',
        'css_files': ['presentation.css'],
        'js_files': ['presentation.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/presentation/presentation.html')
