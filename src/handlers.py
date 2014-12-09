# -*- coding: UTF-8 -*-

import re

from os.path import abspath, join as joinpath, \
                    sep as pathsep, isdir, \
                    exists as pathexists, isfile
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

    def validate_absolute_path(self, root, absolute_path):
        root = abspath(root)
        # os.path.abspath strips a trailing /
        # it needs to be temporarily added back for requests
        # to root/
        abspath_sw = (absolute_path + pathsep).startswith
        sw_root = abspath_sw(root)
        sw_any = any(abspath_sw(group_root)
                     for group_root in self.groups.values())
        if not sw_root and not sw_any:
            raise HTTPError(403,
                '%s is not in root static directory or' \
                'any group root.', self.path)
                
        if (isdir(absolute_path) and
                self.default_filename is not None):
            # need to look at the request.path here for when
            # path is empty but there is some prefix to the
            # path that was already trimmed by the routing
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/",
                              permanent=True)
                return
            absolute_path = joinpath(absolute_path,
                                     self.default_filename)
                                     
        if not pathexists(absolute_path):
            raise HTTPError(404)
            
        if not os.path.isfile(absolute_path):
            raise HTTPError(403, "%s is not a file", self.path)
            
        return absolute_path
