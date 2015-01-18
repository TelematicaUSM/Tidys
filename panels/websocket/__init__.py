import src


class Websocket(src.boiler_ui_module.BoilerUIModule):
    _id = 'Websocket'
    name = 'Websocket Demo'
    conf = {
        'static_url_prefix': '/wspanel/',
        'static_path': './panels/websocket/static',
        'css_files': [],
        'js_files': ['ws.js'],
    }
    
    def render(self):
        return self.render_string(
            '../panels/websocket/demo.html', _id=self._id)


class RedBlackEcho(src.wsclass.WSClass):
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
