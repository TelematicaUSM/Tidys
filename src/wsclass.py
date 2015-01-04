from logging import debug

class WSClass(object):
    def __init__(self, handler):
        self.handler = handler
        
        for attr_name in dir(self):
            attribute = getattr(self, attr_name)
            if hasattr(attribute, 'msg_type'):
                debug('src.swclass.SWClass.__init__: '
                      'Adding action: %r ...' % attribute)
                handler.register_action(attribute.msg_type,
                                        attribute)
    
    class subscribe(object):
        def __init__(self, msg_type):
            self.msg_type = msg_type
        
        def __call__(self, method):
            debug('src.swclass.SWClass.subscribe.__call__: '
                  'Subscribing method %r to %r message '
                  'types ...', method, self.msg_type)
            method.msg_type = self.msg_type
            return method
