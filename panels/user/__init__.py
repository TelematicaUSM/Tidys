import src, jwt

from tornado.gen import coroutine
from src import messages
from src.db import User, Code, NoObjectReturnedFromDB


class UserPanel(src.boiler_ui_module.BoilerUIModule):
    _id = 'user-panel'
    classes = {'scrolling-panel', 'system-panel'}
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
        
    @src.wsclass.WSClass.subscribe('getUserName')
    def get_user_name(self, message):
        try:
            name = self.handler.user.name
            self.handler.write_message({'type': 'userName',
                                        'name': name})
        except AttributeError:
            self.send_error('userNotLoaded', message,
                            'There was no loaded user '
                            'when this message arrived.')
    
    @src.wsclass.WSClass.subscribe('roomCode')
    @coroutine
    def load_room_code(self, message):
        try:
            room_code = yield Code(message['room_code'])
            self.handler.room_code = room_code
            self.handler.write_message(
                {'type': 'roomCodeOk',
                 'code_type': room_code.code_type.value})
                
        except KeyError:
            self.handler.send_malformed_message_error(
                message)
                
        except NoObjectReturnedFromDB:
            self.handler.send_error('codeNotPresentInDB',
                                    message,
                                    'This code is not '
                                    'present in the '
                                    'database.')
