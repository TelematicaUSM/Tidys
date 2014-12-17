import tornado

from tornado.web import StaticFileHandler


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
    
    def javascript_files(self):
        """Returns a list of JavaScript files required by
        this module."""
        return [
            self.make_static_url(path)
            for path in self.conf['js_files']
        ]

    def css_files(self):
        """Returns a list of CSS files required by this
        module."""
        return [
            self.make_static_url(path)
            for path in self.conf['css_files']
        ]

    def make_static_url(self, path):
        return StaticFileHandler.make_static_url(self.conf,
                                                 path)

    def render_string(self, path, **kwargs):
        """Renders a template and returns it as a string."""
        return self.handler.render_string(path,
            make_static_url=self.make_static_url, **kwargs)
