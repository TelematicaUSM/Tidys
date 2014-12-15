import tornado


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
