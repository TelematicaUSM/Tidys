# -*- coding: UTF-8 -*-

from urllib.parse import urlunparse
from . import log

app_name = 'TornadoBoxes'
author = 'Cristóbal Ganter'
author_email = 'cganterh@gmail.com'
debug = True
port = 52001

proxy_scheme = 'http'
proxy_host = 'localhost'
proxy_port = port
_netloc = proxy_host + (':' + str(proxy_port)
                        if proxy_port else '')
proxy_url = urlunparse(
    (proxy_scheme, _netloc, '', '', '', '')
)

user_scalable_viewport = 'no'    #accepted values are 'yes'
                                 #and 'no'
ws_scheme = 'ws'
