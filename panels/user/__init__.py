import src, jwt

from tornado.gen import coroutine
from src import messages
from src.db import User, NoObjectReturnedFromDB


class UserPanel(src.boiler_ui_module.BoilerUIModule):
    _id = 'user-panel'
    _class = 'scrolling-panel'
    name = 'Usuario'
    conf = {
        'static_url_prefix': '/user/',
        'static_path': './panels/user/static',
        'css_files': ['user.css'],
        'js_files': ['user.js'],
    }
    
    def render(self):
        return self.render_string(
            '../panels/user/user.html')


class UserWSC(src.wsclass.WSClass):
    @src.wsclass.WSClass.subscribe('sessionToken')
    @coroutine
    def check_token(self, message):
        try:
            uid = jwt.decode(message['token'],
                             verify=False)['id']
            user = yield User(uid)
            jwt.decode(message['token'], user.secret)
            self.handler.user = user
            self.handler.write_message({'type': 'tokenOk'})
            
        except (jwt.ExpiredSignatureError, jwt.DecodeError,
                NoObjectReturnedFromDB):
            self.handler.write_message({'type': 'logout'})
            
        except:
            messages.unexpected_error(
                'panels.user.UserWSC.check_token')
            raise
        
    @src.wsclass.WSClass.subscribe('getUserName')
    def get_user_name(self, message):
        name = self.handler.user.name
        self.handler.write_message({'type': 'userName',
                                    'name': name})
