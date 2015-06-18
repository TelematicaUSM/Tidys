import src
from src.wsclass import subscribe


class RedBlackEchoPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'red_black_echo'
    classes = {'scrolling-panel'}
    name = 'Red-Black Echo'
    conf = {
        'static_url_prefix': '/rbe/',
        'static_path': './panels/red_black_echo/static',
        'css_files': [],
        'js_files': ['rbe.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/red_black_echo/rbe.html')


class RedBlackEchoWSC(src.wsclass.WSClass):
    @subscribe('red', channels={'w'})
    def return_red(self, message):
        self.handler.ws_pub_sub.send_message({
            'type': 'white',
            'string': 'Red said: "%s"' % message['string']
        })

    @subscribe('black', channels={'w'})
    def return_black(self, message):
        self.handler.ws_pub_sub.send_message({
            'type': 'white',
            'string': 'Black said: "%s"' % message['string']
        })
