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
from pymongo import ASCENDING

from src.utils import standard_name
from .common import db
from .db_object import DBObject


class Course(DBObject):
    coll = db.courses
    path = 'src.db.course.Course'

    @property
    def name(self):
        return self._data['name']

    def __str__(self):
        return self.name

    @classmethod
    @coroutine
    def create(cls, user, name):
        id_ = str(user.id) + standard_name(name)

        self = yield super().create(id_)
        yield self.store_dict(
            {'name': name, 'user_id': user.id})
        return self

    @classmethod
    @coroutine
    def get_user_courses(cls, user):
        """Get all curses created by ``user``.

        :param User user:
            The user who created the courses to be obtained.

        :return:
            A future that resolves to a list of couses.
        """
        try:
            yield cls.coll.ensure_index(
                [('user_id', ASCENDING), ('_id', ASCENDING)]
            )

            courses = yield cls.get_list(
                spec={'user_id': user.id}, fields=['name'])
            return courses

        except:
            raise

    @classmethod
    @coroutine
    def get_courses_from_ids(cls, ids):
        """Get all courses specified by the ids parameter.

        :param list ids:
            A list of the IDs of the documents to be
            fetched.

        :return:
            A future that resolves to a list of courses.
        """
        try:
            courses = yield cls.get_list(
                {
                    '_id': {'$in': ids}
                }
            )
            return courses

        except:
            raise

    @coroutine
    def count_students(self):
        """Count the number of students in this course.

        :return:
            The number of students currently participating
            in this course.
        :rtype:
            A future that resolves to ``int``.

        :raises OperationFailure:
            On a database error.
        """
        try:
            yield db.users.ensure_index(
                [
                    ('course_id', ASCENDING),
                    ('status', ASCENDING)
                ],
                sparse=True
            )

            cursor = db.users.find(
                {'course_id': self.id, 'status': 'seat'})
            count = yield cursor.count()
            return count

        except:
            raise
