# -*- coding: UTF-8 -*-

import re

from os.path import abspath, join as joinpath
from tornado.web import StaticFileHandler

class FileGoupsHandler(StaticFileHandler):
    groups = {}
    match = re.compile('^_(.+)_/(.+)$').match
    
    @classmethod
    def get_absolute_path(cls, root, path):
        mobject = cls.match(path)
        
        if mobject:
            group_id = mobject.group(1)
            path = mobject.group(2)
            group_root = cls.groups[group_id]
            return abspath(joinpath(group_root, path))
        else:
            return abspath(joinpath(root, path))
    
    @classmethod
    def register_group(cls, group_id, group_root):
        cls.groups[group_id] = group_root
