# -*- coding: UTF-8 -*-

from tornado.gen import coroutine

import src
from src.wsclass import subscribe


class SlidesPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'slides-panel'
    classes = {'scrolling-panel', 'teacher-panel'}
    name = 'Diapositivas'
    conf = {
        'static_url_prefix': '/slides/',
        'static_path': './panels/slides/static',
        'css_files': ['slides.css'],
        'js_files': ['slides.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/slides/slides.html')


class SlidesWSC(src.wsclass.WSClass):
    pass
