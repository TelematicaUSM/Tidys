import tornado

from tornado.web import StaticFileHandler


class IncludeExtFiles(tornado.web.UIModule):
    def render(self):
        return ''
    
    def get_urls(self, file_extension):
        if hasattr(self.handler, 'ext_files'):
            ext_files = [self.handler.static_url(fn)
                         for fn in self.handler.ext_files
                         if '.'+file_extension in fn]
        else:
            ext_files = []
            
        # Para incluir archivos de un modulo, el handler
        # tiene que heredar de src.handlers.ModuleHandler.
        if hasattr(self.handler, 'module_files') and \
           hasattr(self.handler, 'module_url'):
            module_files = [self.handler.module_url(fn)
                for fn in self.handler.module_files
                if '.'+file_extension in fn]
        else:
            module_files = []
        
        return module_files + ext_files
            
    def css_files(self):
        return self.get_urls('css')
        
    def javascript_files(self):
        return self.get_urls('js')


class UIModule(tornado.web.UIModule):
    def __init__(self, handler):
        super().__init__(handler)
        self.application = handler.application
        self.config()
        if self.config.static_root:
            self.application.add_handlers('.*$',
                [(self.config.static_url_prefix + '(.*)',
                  StaticFileHandler,
                  {'path': self.config.static_root})])
    
    def config(self):
        self.config.static_url_prefix = '/static/'
        self.config.static_root = ''
        self.config.css_files = []
        self.config.js_files = []
        
    def render(self, set_resources=None):
        if set_resources:
            set_resources(
                javascript_files=self.config.js_files,
                css_files=self.config.css_files)
    
    def javascript_files(self):
        """Returns a list of JavaScript files required by
        this module."""
        return self.config.js_files

    def css_files(self):
        """Returns a list of CSS files required by this
        module."""
        return self.config.css_files
