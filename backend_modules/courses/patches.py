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
