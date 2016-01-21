#!/usr/bin/env python3
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


"""Print the tarball's url of virtualenv to stdout.

.. todo::
    * Add cli's atribute support.
"""


def get_pypi_package_url(package_name='virtualenv'):
    """Return the tarball's url of a package.

    :param str package_name: The name of the package.

    :return: The tarball's url of the package.
    """
    import json
    from urllib.request import urlopen

    url = 'http://pypi.python.org/pypi/{}/json'.format(
        package_name)
    response = urlopen(url).read().decode('utf-8')
    return next(
        url['url']
        for url in json.loads(response)['urls']
        if url['url'].endswith('tar.gz')
    )

if __name__ == '__main__':
    print(
        get_pypi_package_url('virtualenv')
    )
