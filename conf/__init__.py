# -*- coding: UTF-8 -*-

""".. todo:: Describe secret files origin and format."""

from os import environ, path

from urllib.parse import urlunparse

from . import log  # noqa

app_name = 'EduRT'
app_logo_path = './art/favicon/2logo.png'
author = 'Cristóbal Ganter'
author_email = 'cganterh@gmail.com'
login_path = 'signin'

# TORNADO
autoreload = False
debug = True
port = 52004

proxy_scheme = 'http'
proxy_host = 'aka.aa.cganterh.net'
proxy_port = None
"""Should be ``int`` or None. This is the port you use to
connect from the outside."""

_netloc = proxy_host + (':' + str(proxy_port)
                        if proxy_port else '')
proxy_url = urlunparse(
    (proxy_scheme, _netloc, '', '', '', '')
)

# CLIENT SPECIFIC:
ws_scheme = 'ws'

ws_reconnect_interval = 55
"""In seconds. See
`<https://github.com/joewalnes/reconnecting-websocket
#reconnectinterval>`_."""

user_scalable_viewport = 'no'
"""Accepted values are ``'yes'`` and ``'no'``."""

# SERVER SPECIFIC:
root_path = environ.get('AA_PATH', '')

secrets_file = path.join(
    root_path,
    'secrets/secrets.json'
)

google_secrets_file = path.join(
    root_path,
    'secrets/client_secret_183281382160-'
    'p087nib71k6besmit0krm07qbsknharp'
    '.apps.googleusercontent.com.json'
)

ping_sleep = 10
"""In seconds. See :meth:`~controller.MSGHandler.on_pong`"""

ping_timeout = 20
"""In seconds. See :meth:`~controller.MSGHandler.on_pong`"""

database_name = 'artalan'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
