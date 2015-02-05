import src, jwt

from sys import exc_info
from logging import error
from tornado.gen import coroutine
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
    def checkToken(self, message):
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
        
        except NameError as e:
            error('#el error es %s', e)
            
        except:
            error('panels.user.UserWSC.checkToken: '
                  'Unexpected error: %s', exc_info()[0])
            raise
        
    @src.wsclass.WSClass.subscribe('getUserEMail')
    def getUserEMail(self, message):
        email = self.handler.user.email
        self.handler.write_message({'type': 'userEMail',
                                    'email': email})
