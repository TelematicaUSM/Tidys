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


from unittest import TestCase

from panels import user


class TruthTableTestCase(TestCase):
    def assertTruthTable(
            self, function, table, message=None):
        for row in table:
            with self.subTest(row=row):
                self.assertEqual(
                    function(*row[:-1]),
                    row[-1],
                    "{f.__qualname__} doesn't respect the "
                    "row {r} of the truth "
                    "table.".format(f=function, r=row)
                )


class TestUserWSC(TruthTableTestCase):
    def test_should_run_room_deassign_course(self):
        """ Test ``should_run_room_deassign_course``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.should_run_room_deassign_course,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 1, 0),
                (0, 1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 1, 1, 0),

                (0, 0, 1, 0, 1, 0, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 1, 0),
                (0, 0, 1, 0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1, 0),

                (1, 0, 1, 0, 1, 0, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 1, 0),
                (1, 0, 1, 0, 0, 0, 1, 0, 0),
                (1, 0, 1, 0, 0, 0, 1, 1, 0),

                (0, 0, 0, 1, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 1, 0),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 0),

                (1, 0, 0, 1, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 0, 1),
                (1, 0, 0, 1, 0, 1, 0, 1, 1),
                (1, 0, 0, 1, 0, 0, 1, 0, 0),
                (1, 0, 0, 1, 0, 0, 1, 1, 1),
            ]
        )

    def test_should_run_user_deassign_course(self):
        """ Test ``should_run_user_deassign_course``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.should_run_user_deassign_course,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 1, 0),
                (0, 1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 1, 1, 0),

                (0, 0, 1, 0, 1, 0, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 1, 0),
                (0, 0, 1, 0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1, 0),

                (1, 0, 1, 0, 1, 0, 0, 0, 1),
                (1, 0, 1, 0, 0, 1, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 1, 1),
                (1, 0, 1, 0, 0, 0, 1, 0, 1),
                (1, 0, 1, 0, 0, 0, 1, 1, 1),

                (0, 0, 0, 1, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 1, 0),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 0),

                (1, 0, 0, 1, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 0, 1),
                (1, 0, 0, 1, 0, 1, 0, 1, 1),
                (1, 0, 0, 1, 0, 0, 1, 0, 0),
                (1, 0, 0, 1, 0, 0, 1, 1, 1),
            ]
        )

    def test_should_run_use_seat(self):
        """ Test ``should_run_use_seat``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.should_run_use_seat,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 1),
                (0, 1, 0, 0, 0, 1, 0, 1, 1),
                (0, 1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 1, 1, 0),

                (0, 0, 1, 0, 1, 0, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 0, 1),
                (0, 0, 1, 0, 0, 1, 0, 1, 1),
                (0, 0, 1, 0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1, 0),

                (1, 0, 1, 0, 1, 0, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 0, 1),
                (1, 0, 1, 0, 0, 1, 0, 1, 1),
                (1, 0, 1, 0, 0, 0, 1, 0, 0),
                (1, 0, 1, 0, 0, 0, 1, 1, 0),

                (0, 0, 0, 1, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 1),
                (0, 0, 0, 1, 0, 1, 0, 1, 1),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 0),

                (1, 0, 0, 1, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 0, 1),
                (1, 0, 0, 1, 0, 1, 0, 1, 1),
                (1, 0, 0, 1, 0, 0, 1, 0, 0),
                (1, 0, 0, 1, 0, 0, 1, 1, 0),
            ]
        )

    def test_should_run_logout_other_instances(self):
        """ Test ``should_run_logout_other_instances``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.should_run_logout_other_instances,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 1),
                (0, 1, 0, 0, 0, 1, 0, 1, 1),
                (0, 1, 0, 0, 0, 0, 1, 0, 1),
                (0, 1, 0, 0, 0, 0, 1, 1, 1),

                (0, 0, 1, 0, 1, 0, 0, 0, 1),
                (0, 0, 1, 0, 0, 1, 0, 0, 1),
                (0, 0, 1, 0, 0, 1, 0, 1, 1),
                (0, 0, 1, 0, 0, 0, 1, 0, 1),
                (0, 0, 1, 0, 0, 0, 1, 1, 1),

                (1, 0, 1, 0, 1, 0, 0, 0, 1),
                (1, 0, 1, 0, 0, 1, 0, 0, 1),
                (1, 0, 1, 0, 0, 1, 0, 1, 1),
                (1, 0, 1, 0, 0, 0, 1, 0, 1),
                (1, 0, 1, 0, 0, 0, 1, 1, 1),

                (0, 0, 0, 1, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 1),
                (0, 0, 0, 1, 0, 1, 0, 1, 1),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 1),

                (1, 0, 0, 1, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 0, 1),
                (1, 0, 0, 1, 0, 1, 0, 1, 1),
                (1, 0, 0, 1, 0, 0, 1, 0, 0),
                (1, 0, 0, 1, 0, 0, 1, 1, 1),
            ]
        )

    def test_should_run_load_course(self):
        """ Test ``should_run_load_course``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.should_run_load_course,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 1, 0),
                (0, 1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 1, 1, 0),

                (0, 0, 1, 0, 1, 0, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 1, 0),
                (0, 0, 1, 0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1, 0),

                (1, 0, 1, 0, 1, 0, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 0, 1),
                (1, 0, 1, 0, 0, 1, 0, 1, 0),
                (1, 0, 1, 0, 0, 0, 1, 0, 0),
                (1, 0, 1, 0, 0, 0, 1, 1, 0),

                (0, 0, 0, 1, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 1, 0),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 0),

                (1, 0, 0, 1, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 1, 0),
                (1, 0, 0, 1, 0, 0, 1, 0, 1),
                (1, 0, 0, 1, 0, 0, 1, 1, 0),
            ]
        )

    def test_should_run_redirect_to_teacher_view(self):
        """ Test ``should_run_redirect_to_teacher_view``.

        Inputs are tuples of the form::

            (has_course, was_none, was_student, was_teacher,
             is_none, is_student, is_teacher, distinct_room)
        """
        self.assertTruthTable(
            user.UserWSC.
            should_run_redirect_to_teacher_view,
            [
                (0, 1, 0, 0, 1, 0, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 0, 1, 0, 1, 0),
                (0, 1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 1, 1, 0),

                (0, 0, 1, 0, 1, 0, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0, 1, 0),
                (0, 0, 1, 0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0, 1, 1, 0),

                (1, 0, 1, 0, 1, 0, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 0, 0),
                (1, 0, 1, 0, 0, 1, 0, 1, 0),
                (1, 0, 1, 0, 0, 0, 1, 0, 0),
                (1, 0, 1, 0, 0, 0, 1, 1, 0),

                (0, 0, 0, 1, 1, 0, 0, 0, 1),
                (0, 0, 0, 1, 0, 1, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 1, 0),
                (0, 0, 0, 1, 0, 0, 1, 0, 0),
                (0, 0, 0, 1, 0, 0, 1, 1, 0),

                (1, 0, 0, 1, 1, 0, 0, 0, 1),
                (1, 0, 0, 1, 0, 1, 0, 0, 0),
                (1, 0, 0, 1, 0, 1, 0, 1, 0),
                (1, 0, 0, 1, 0, 0, 1, 0, 0),
                (1, 0, 0, 1, 0, 0, 1, 1, 0),
            ]
        )
