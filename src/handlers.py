# -*- coding: UTF-8 -*-

from tornado.web import RequestHandler, StaticFileHandler

class ModuleHandler(RequestHandler):

    """RequestHandler que implementa module_url.
    
    module_url es un metodo similar a static_url que permite incluir
    archivos que no se encuentran en el static_path de la aplicacion.
    
    Las clases que hereden de ModuleHandler deben definir
    self.static_path y self.static_url_prefix en el metodo de
    inicializacion (__init__).
    
    Esta clase esta pensada para crear modulos independientes de la
    aplicacion, que pueden servir sus propios archivos estaticos.
    Ver ejemplo en src/qrmaker."""
    
    def module_url(self, path, include_host=None, **kwargs):
        get_url = self.settings.get("static_handler_class",
                                    StaticFileHandler).make_static_url

        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""

        return base + get_url(
            {'static_path': self.static_path,
             'static_url_prefix': self.static_url_prefix},
            path, **kwargs)
