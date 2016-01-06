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


from string import ascii_lowercase, digits
from enum import Enum
from xml.etree import ElementTree
from tornado.gen import coroutine
from pymongo.errors import DuplicateKeyError, \
    OperationFailure
from src import messages as msg
from src.utils import run_in_thread, random_word
from .common import db, NoObjectReturnedFromDB, \
    ConditionNotMetError
from .db_object import DBObject


NS = {'svg': 'http://www.w3.org/2000/svg'}
_path = 'src.db.room'


class Room(DBObject):
    coll = db.rooms
    _path = msg.join_path(_path, 'Room')
    defaults = {}

    @classmethod
    @coroutine
    def create(cls, name, svg_path):
        try:
            _path = msg.join_path(cls._path, 'create')

            ElementTree.register_namespace('', NS['svg'])
            elem_tree = yield run_in_thread(
                ElementTree.parse, svg_path)

            seat_circles = elem_tree.iterfind(
                ".//svg:circle[@class='seat']", NS)
            seat_attributes = (c.attrib
                               for c in seat_circles)
            seats = {a['id']: {'used': False,
                               'x': a['cx'],
                               'y': a['cy']}
                     for a in seat_attributes}

            self = yield super().create(name)
            self.setattr(
                '_map', elem_tree.getroot()
            )
            yield self.store_dict(
                {
                    'map_source': ElementTree.tostring(
                        self.map, encoding="unicode"),
                    'seats': seats
                }
            )

            code = yield Code.create(
                room_id=self.id, code_type=CodeType.room)

            codes = [code]
            for seat in self.seats:
                code = yield Code.create(
                    room_id=self.id,
                    code_type=CodeType.seat,
                    seat_id=seat
                )
                codes.append(code)

            return (self, codes)

        except DuplicateKeyError:
            raise

        except OperationFailure:
            msg.obj_creation_error(_path, cls, name=name,
                                   svg_path=svg_path)
            cls.coll.remove(name)
            raise

    def __str__(self):
        return self.name

    @coroutine
    def assign_course(self, course_id):
        """Adds a course from the courses set.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.
        """
        yield self.modify(
            {
                '$addToSet': {'courses': course_id}
            }
        )

    @coroutine
    def deassign_course(self, course_id):
        """Remove a course from the courses set.

        :raises ConditionNotMetError:
            If the document no longer exists in the
            database.
        """
        yield self.modify(
            {
                '$pull': {'courses': course_id}
            }
        )

    @coroutine
    def _modify_seat(self, seat_id, use):
        try:
            used = 'seats.{}.used'.format(seat_id)
            yield self.modify_if(
                {used: not use},
                {
                    '$set': {used: use}
                }
            )
        except ConditionNotMetError as e:
            cnme = ConditionNotMetError(
                'The seat {} is{} used.'.format(
                    seat_id, '' if use else ' not')
            )
            raise cnme from e

    @coroutine
    def use_seat(self, seat_id):
        yield self._modify_seat(seat_id, use=True)

    @coroutine
    def leave_seat(self, seat_id):
        yield self._modify_seat(seat_id, use=False)

    @property
    def name(self):
        return self.id

    @property
    def map(self):
        if not hasattr(self, '_map'):
            self.setattr(
                '_map',
                ElementTree.fromstring(self.map_source)
            )
        return self._map


class CodeType(Enum):
    room = 'room'
    seat = 'seat'


class Code(DBObject):

    """Interface to the ``codes`` collection.

    .. todo::
        * Review error handling.
    """

    coll = db.codes
    _path = msg.join_path(_path, 'Code')

    @classmethod
    @coroutine
    def _gen_new_code(cls):
        for i in range(200):
            try:
                code = random_word(
                    5, ascii_lowercase + digits)
                self = yield super().create(code)
                return (self, code)

            except DuplicateKeyError:
                msg.try_new_id_after_dup_obj_in_db(
                    cls.path + '.create')
        else:
            msg.exhausted_tries(cls.path + '.create')

    @classmethod
    @coroutine
    def create(cls, room_id, code_type, seat_id=None):
        """Create a new code.

        .. todo::
            *   review error handling.
        """
        _path = msg.join_path(cls._path, 'create')

        def creat_err_msg():
            msg.obj_creation_error(_path, cls,
                                   room_id=room_id,
                                   code_type=code_type,
                                   seat_id=seat_id)

        if not isinstance(code_type, CodeType):
            raise TypeError

        if seat_id is not None and \
                not isinstance(seat_id, str):
            raise TypeError

        if (code_type is CodeType.room) == \
                (seat_id is not None):
            raise ValueError

        try:
            # Throws NoObjectReturnedFromDB
            room = yield Room.get(room_id)

            self, code = yield cls._gen_new_code()
            self.setattr('_room', room)

            # Throws OperationFailure
            yield self.store_dict(
                {'room_id': room_id,
                 'code_type': code_type.value,
                 'seat_id': seat_id})
            return self

        except NoObjectReturnedFromDB:
            creat_err_msg()
            raise OperationFailure

        except OperationFailure:
            creat_err_msg()
            cls.coll.remove(code)
            raise

    def __str__(self):
        return '<%s -> (%s, %s)>' % (self.id, self.room_id,
                                     self.seat_id)

    @property
    @coroutine
    def room(self):
        if not hasattr(self, '_room'):
            room = yield Room.get(self.room_id)
            self.setattr('_room', room)
        return self._room

    @property
    def code_type(self):
        return CodeType(self._data['code_type'])
