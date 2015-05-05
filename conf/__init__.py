# -*- coding: UTF-8 -*-

from urllib.parse import urlunparse
from . import log

app_name = 'ArtificialAlan'
app_logo_path = './art/favicon/2logo.png'
author = 'Cristóbal Ganter'
author_email = 'cganterh@gmail.com'
debug = True
port = 52002
login_path = 'signin'

proxy_scheme = 'http'
#proxy_host = 'mem.zoro.cganterh.net'
proxy_host = 'mem.robin.cganterh.net'
proxy_port = None
_netloc = proxy_host + (':' + str(proxy_port)
                        if proxy_port else '')
proxy_url = urlunparse(
    (proxy_scheme, _netloc, '', '', '', '')
)

#CLIENT SPECIFIC:
ws_scheme = 'ws'
user_scalable_viewport = 'no'    #accepted values are 'yes'
                                 #and 'no'

#SERVER SPECIFIC:
#secrets_file = 'secrets/secrets.json'
#google_secrets_file = 'secrets/client_secret_157405624098' \
#                      '-rfhsi6ovr7lugc0f1u84ntuoufpmsfjr.' \
#                      'apps.googleusercontent.com.json'
secrets_file = 'secrets_robin/secrets.json'
google_secrets_file = 'secrets_robin/client_secret_'\
                      '574237562896-8fc1unhpaqr5idf7bamouq'\
                      'r7l4ruvik1.apps.googleusercontent'\
                      '.com.json'
database_name = 'artalan'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
