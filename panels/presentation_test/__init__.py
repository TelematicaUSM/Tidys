import src


class RemoteTestPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'presentation_test'
    classes = {'scrolling-panel', 'system'}
    name = 'Presentation Test'

    def render(self):
        return self.render_string(
            '../panels/presentation_test/presentation_test.html')
