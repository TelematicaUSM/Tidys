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
proxy_host = 'mem.zoro.cganterh.net'
# proxy_host = 'mem.robin.cganterh.net'
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
_z_secrets_file = 'secrets/secrets.json'
_z_google_secrets_file = 'secrets/' \
    'client_secret_157405624098-' \
    'rfhsi6ovr7lugc0f1u84ntuoufpmsfjr.apps.' \
    'googleusercontent.com.json'
_r_secrets_file = 'secrets_robin/secrets.json'
_r_google_secrets_file = 'secrets_robin/client_secret_'\
    '574237562896-8fc1unhpaqr5idf7bamouqr7l4ruvik1.apps.' \
    'googleusercontent.com.json'

secrets_file = path.join(root_path, _z_secrets_file)
google_secrets_file = path.join(root_path,
                                _z_google_secrets_file)

database_name = 'artalan'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
