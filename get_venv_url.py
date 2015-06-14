#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

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
