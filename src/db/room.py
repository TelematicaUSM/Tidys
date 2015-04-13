# -*- coding: UTF-8 -*-

from string import ascii_lowercase, digits
from enum import Enum
from xml.etree import ElementTree
from tornado.gen import coroutine
from pymongo.errors import DuplicateKeyError, \
                           OperationFailure
from src import messages as msg
from src.utils import run_in_thread, random_word
from .common import db, NoObjectReturnedFromDB
from .db_object import DBObject


NS = {'svg': 'http://www.w3.org/2000/svg'}


class Room(DBObject):
    coll = db.rooms
    path = 'src.db.room.Room'
    
    @classmethod
    @coroutine
    def create(cls, name, svg_path):
        try:
            code_path = cls.path + '.create'
            
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
                {'map_source':
                    ElementTree.tostring(self.map,
                        encoding="unicode"),
                 'seats': seats})
            
            code = yield Code.create(room_id=self.id,
                code_type=CodeType.room)
            
            codes = [code]
            for seat in self.seats:
                code = yield Code.create(room_id=self.id,
                    code_type=CodeType.seat, seat_id=seat)
                codes.append(code)
                
            return (self, codes)
            
        except DuplicateKeyError:
            raise
            
        except OperationFailure:
            msg.obj_creation_error(code_path, cls,
                                   name=name,
                                   svg_path=svg_path)
            cls.coll.remove(name)
            raise
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Room('%s')" % self.id
    
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
    from .room import Room
    room = 'room'
    seat = 'seat'


class Code(DBObject):
    coll = db.codes
    path = 'src.db.code.Code'
    
    @classmethod
    @coroutine
    def create(cls, room_id, code_type, seat_id=None):
        code_path = cls.path + '.create'
        creat_err_msg = lambda: msg.obj_creation_error(
            code_path, cls, room_id=room_id,
            code_type=code_type, seat_id=seat_id)
            
        if not isinstance(code_type, CodeType):
            raise TypeError
        
        if seat_id and not isinstance(seat_id, str):
            raise TypeError
        
        if (code_type is CodeType.room) == bool(seat_id):
            raise ValueError
        
        try:
            #Throws NoObjectReturnedFromDB
            room = yield Room(room_id)
                
            for i in range(200):
                try:
                    code = random_word(5,
                        ascii_lowercase+digits)
                    self = yield super().create(code)
                    break
                    
                except DuplicateKeyError:
                    msg.try_new_id_after_dup_obj_in_db(
                        cls.path+'.create')
            else:
                msg.exhausted_tries(cls.path+'.create')
            
            self.setattr('_room', room)
            #Trhows OperationFailure
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
    
    def __repr__(self):
        return "Code('%s')" % self.id
    
    @property
    @coroutine
    def room(self):
        if not hasattr(self, '_room'):
            room = yield Room(self.room_id)
            self.setattr('_room', room)
        return self._room
