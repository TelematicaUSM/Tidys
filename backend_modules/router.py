# -*- coding: UTF-8 -*-

import src
from src.wsclass import subscribe
from src import messages as msg

_path = 'backend_modules.router'


class RouterWSC(src.wsclass.WSClass):
    _path = msg.join_path(_path, 'RouterWSC')

    @subscribe('toFrontend', channels={'l', 'd'})
    def to_frontend(self, message):
        self.redirect_content_to('w', message)

    @subscribe('toDatabase', channels={'l'})
    def to_database(self, message):
        self.redirect_content_to('d', message)

    @subscribe('toLocal', channels={'d'})
    def to_local(self, message):
        self.redirect_content_to('l', message)
