# -*- coding: UTF-8 -*-

""".. todo:: Describe secret files origin and format."""

from os import environ, path

from urllib.parse import urlunparse

from . import log

app_name = 'ArtificialAlan'
app_logo_path = './art/favicon/2logo.png'
author = 'Cristóbal Ganter'
author_email = 'cganterh@gmail.com'
login_path = 'signin'

# TORNADO
autoreload = False
debug = True
port = 52002

proxy_scheme = 'http'
proxy_host = 'aka.aa.cganterh.net'
proxy_port = None
_netloc = proxy_host + (':' + str(proxy_port)
                        if proxy_port else '')
proxy_url = urlunparse(
    (proxy_scheme, _netloc, '', '', '', '')
)

# CLIENT SPECIFIC:
ws_scheme = 'ws'

ws_reconnect_interval = 20
"""In seconds. See """

# accepted values are 'yes' and 'no'
user_scalable_viewport = 'no'

# SERVER SPECIFIC:
root_path = environ.get('AA_PATH', '')

secrets_file = path.join(root_path, _z_secrets_file)
google_secrets_file = path.join(root_path,
                                _z_google_secrets_file)

database_name = 'artalan'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
