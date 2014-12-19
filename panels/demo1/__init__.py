import src


class Demo(src.boiler_ui_module.BoilerUIModule):
    _id = 'demo1'
    name = 'Demo 1'
    
    def render(self):
        return self.render_string(
            '../panels/demo/demo.html', _id=self._id)
