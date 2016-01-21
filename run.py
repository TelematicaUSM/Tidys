# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from tornado.gen import coroutine

from src.utils import run_inside

ioloop = None
t = None


def start():
    global ioloop, t
    import controller  # noqa
    from threading import Thread
    from tornado.ioloop import IOLoop
    from src import messages

    messages.starting()

    ioloop = IOLoop.instance()
    t = Thread(target=lambda: ioloop.start())
    t.start()

    messages.welcome()


def stop():
    from src import messages

    @coroutine
    def callback():
        from controller import MSGHandler
        from src import db
        yield MSGHandler.stop()
        yield db.stop()
        ioloop.stop()

    ioloop.add_callback(callback)
    t.join()

    messages.stopped()

if __name__ == "__main__":  # noqa
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

    @run_inside(ioloop.add_callback)
    def clients():
        from controller import MSGHandler
        total = MSGHandler.client_count
        current = len(MSGHandler.clients)
        print('Connected clients: %d' % current)
        print('Total connections opened: %d' % total)
        print(
            'Total connections closed: %d' %
            (total - current)
        )

    @run_inside(ioloop.add_callback)
    def bcast(message):
        from controller import MSGHandler
        MSGHandler.broadcast(message)

    @run_inside(ioloop.add_callback)
    @coroutine
    def add_room(room_name, svg_path,
                 output_path='./qrmaster'):
        import src.utils.qrmaster as qrm
        from pymongo.errors import OperationFailure
        from conf import app_name, proxy_url, app_logo_path
        from src.db.room import Room, CodeType

        try:
            _, code_objs = yield Room.create(room_name,
                                             svg_path)
            codes = (
                [
                    c.id,
                    c.room_id if c.code_type ==
                    CodeType.room.value else c.seat_id
                ]
                for c in code_objs
            )
            qrm.generate(codes, url=proxy_url,
                         title=app_name,
                         img_path=app_logo_path,
                         output_path=output_path)

        except OperationFailure:
            pass

    @run_inside(ioloop.add_callback)
    def send_dbm(message):
        import src.db.message_broker as mb
        mb.send_message(message)

    @run_inside(ioloop.add_callback)
    def register_dbm(owner, msg_type, action):
        import src.db.message_broker as mb
        mb.register_action(owner, msg_type, action)

    @run_inside(ioloop.add_callback)
    def remove_owner_dbm(owner):
        import src.db.message_broker as mb
        mb.remove_owner(owner)
