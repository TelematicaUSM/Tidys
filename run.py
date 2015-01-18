# -*- coding: UTF-8 -*-

from threading import Thread
from logging import info
from tornado.ioloop import IOLoop
from conf import app_name, port
from controller import app
from src import cli

info('%s: Starting on port %d ...', app_name, port)
app.listen(port)

ioloop = IOLoop.instance()
t = Thread(target=lambda:ioloop.start())
t.start()

cli.start()

ioloop.add_callback(lambda:ioloop.stop())
t.join()
