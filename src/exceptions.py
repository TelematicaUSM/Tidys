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


class NotDictError(TypeError):
    """Raise when an object is not an instance of dict.

    .. automethod:: __init__
    """

    def __init__(self, name, *args):
        """Initialize a new NotDictError.

        :param str name:
            Name of the object that is not a dictionary.
        """
        super().__init__(
            '{} is not a dictionary.'.format(name),
            *args
        )


class NotStringError(TypeError):
    """Raise when an object is not an instance of str.

    .. automethod:: __init__
    """

    def __init__(self, name, *args):
        """Initialize a new NotStringError.

        :param str name:
            Name of the object that is not a string.
        """
        super().__init__(
            '{} is not a string.'.format(name),
            *args
        )


class MissingFieldError(ValueError):
    """Raise when a dict doesn't have a required field.

    .. automethod:: __init__
    """

    def __init__(self, dict_name, field_name, *args):
        """Initialize a new MissingFieldError.

        :param str dict_name:
            The name of the dictionary.

        :param str field_name:
            The name of the field that is missing in the
            dictionary.
        """
        super().__init__(
            "{} should have a '{}' field.".format(
                dict_name, field_name),
            *args
        )
