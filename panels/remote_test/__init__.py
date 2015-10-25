import src


class RemoteTestPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'remote-test'
    classes = {'scrolling-panel', 'system-panel'}
    name = 'Remote Test'

    def render(self):
        return self.render_string(
            '../panels/remote_test/remote_test.html')
