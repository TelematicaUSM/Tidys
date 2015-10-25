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
port = 54001

proxy_scheme = 'http'
proxy_host = 'dev.pip.aa.cganterh.net'
proxy_port = None
_netloc = proxy_host + (':' + str(proxy_port)
                        if proxy_port else '')
proxy_url = urlunparse(
    (proxy_scheme, _netloc, '', '', '', '')
)

# CLIENT SPECIFIC:
ws_scheme = 'ws'

# accepted values are 'yes' and 'no'
user_scalable_viewport = 'no'

# SERVER SPECIFIC:
root_path = environ.get('AA_PATH', '')
_secrets_file = 'secrets/secrets.json'
_google_secrets_file = 'secrets/' \
    'client_secret_476255121881-8fdc3t0sv2id4pnfdl2htb663s'\
    'dp6e4g.apps.googleusercontent.com.json'

secrets_file = path.join(root_path, _secrets_file)
google_secrets_file = path.join(root_path,
                                _google_secrets_file)

database_name = 'devpipaacganterhnet'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
