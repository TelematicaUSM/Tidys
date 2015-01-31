# -*- coding: UTF-8 -*-

from threading import Thread
from tornado.ioloop import IOLoop
from conf import port
from controller import app
from src import cli, messages


messages.starting()
app.listen(port)

ioloop = IOLoop.instance()
t = Thread(target=lambda:ioloop.start())
t.start()

cli.start()

ioloop.add_callback(lambda:ioloop.stop())
t.join()
