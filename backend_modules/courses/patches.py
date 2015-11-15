#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from controller import MSGHandler
from src.db import Room
from .. import router
from .wsclass import CoursesWSC

Room.defaults['courses'] = []
"""This patches the ``Room`` class, so that it has a
default attribute named ``courses``."""

MSGHandler._course = None


@property
def course(self):
    """Current course asociated with this MSGHandler."""
    return self._course


@course.setter
def course(self, new_course):
    self._course = new_course
    self.course_msg_type = \
        'courseMessage({})'.format(new_course.id)

    router_object = self.ws_objects[
        router.RouterWSC]
    courses_object = self.ws_objects[CoursesWSC]

    courses_object.register_action_in(
        self.course_msg_type,
        action=router_object.to_local,
        channels={'d'}
    )
MSGHandler.course = course
