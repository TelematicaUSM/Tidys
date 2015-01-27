import src


class UI(src.boiler_ui_module.BoilerUIModule):
    _id = 'about'
    _class = 'scrolling-panel'
    name = 'About'
    
    def render(self):
        return self.render_string(
            '../panels/about/about.html')
