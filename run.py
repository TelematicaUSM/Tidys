from signal import signal, SIGINT
from sys import exit
from logging import info
from tornado.ioloop import IOLoop
from conf import app_name, port
from controller import app


def exit_handler(signal, frame):
    info('\n%s: Closing ...', app_name)
    exit(0)
signal(SIGINT, exit_handler)

info('%s: Starting on port %d ...', app_name, port)
app.listen(port)
IOLoop.instance().start()
