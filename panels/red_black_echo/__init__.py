import src


class UI(src.boiler_ui_module.BoilerUIModule):
    _id = 'red_black_echo'
    name = 'Red-Black Echo'
    conf = {
        'static_url_prefix': '/rbe/',
        'static_path': './panels/red_black_echo/static',
        'css_files': [],
        'js_files': ['rbe.js'],
    }
    
    def render(self):
        return self.render_string(
            '../panels/red_black_echo/demo.html')


class WS(src.wsclass.WSClass):
    @src.wsclass.WSClass.subscribe('red')
    def return_red(self, message):
        self.handler.write_message({
            'type': 'white',
            'string': 'Red said: "%s"' % message['string']
        })
    
    @src.wsclass.WSClass.subscribe('black')
    def return_black(self, message):
        self.handler.write_message({
            'type': 'white',
            'string': 'Black said: "%s"' % message['string']
        })
