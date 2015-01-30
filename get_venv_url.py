#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
from urllib.request import urlopen

response = urlopen('http://pypi.python.org/pypi/virtualenv/'
                   'json').read().decode('utf-8')
url = next(
    url['url'] for url in json.loads(response)['urls']
               if url['url'].endswith('tar.gz')
)

print(url)
