import tornado

from tornado.web import StaticFileHandler
from src.ui_methods import add_ext_file


class BoilerUIModule(tornado.web.UIModule):
    conf = {
        'static_url_prefix': '',
        'static_path': '',
        'css_files': [],
        'js_files': [],
    }
    
    @classmethod
    def add_handler(cls, app):
        if cls.conf['static_path'] and \
           cls.conf['static_url_prefix']:
            app.add_handlers(
                '.*$',
                [(
                    cls.conf['static_url_prefix'] + '(.*)',
                    StaticFileHandler,
                    {'path': cls.conf['static_path']}
                )]
            )

    def make_static_url(self, path):
        return StaticFileHandler.make_static_url(self.conf,
                                                 path)

    def render_string(self, path, **kwargs):
        """Renders a template and returns it as a string."""
        add_ext_file(self.handler, self.conf['css_files'],
                     self.make_static_url)
        add_ext_file(self.handler, self.conf['js_files'],
                     self.make_static_url)
            
        return self.handler.render_string(path,
            make_static_url=self.make_static_url, **kwargs)
