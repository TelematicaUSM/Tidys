# -*- coding: UTF-8 -*-

def start():
    global ioloop, t
    import controller
    from tornado.ioloop import IOLoop
    from threading import Thread
    from src import messages
    
    messages.starting()
    
    ioloop = IOLoop.instance()
    t = Thread(target=lambda:ioloop.start())
    t.start()
    
    messages.wellcome()

def stop():
    from src import messages
    
    def callback():
    # Here you can stop other services.
        ioloop.stop()
        
    ioloop.add_callback(callback)
    t.join()
    
    messages.stopped()

if __name__ == "__main__":
    start()

    def q():
        from sys import exit
        stop()
        exit()
    
    def h():
        from sys import modules
        help(modules[__name__])
    
    def make(goal):
        from os import system
        system('make %s' % goal)
