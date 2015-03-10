# -*- coding: UTF-8 -*-

from . import log

app_name = 'ArtificialAlan'
author = 'Cristóbal Ganter'
author_email = 'cganterh@gmail.com'
debug = True
port = 52002

proxy_scheme = 'http'
proxy_host = 'mem.zoro.cganterh.net'
proxy_port = None

#CLIENT SPECIFIC:
ws_scheme = 'ws'
user_scalable_viewport = 'no'    #accepted values are 'yes'
                                 #and 'no'

#SERVER SPECIFIC:
secrets_file = 'secrets/secrets.json'
google_secrets_file = 'secrets/client_secret_157405624098' \
                      '-rfhsi6ovr7lugc0f1u84ntuoufpmsfjr.' \
                      'apps.googleusercontent.com.json'
database_name = 'artalan'
short_account_exp = {'minutes': 5}
long_account_exp = {'days': 30 if not debug else 1}
