# -*- coding: UTF-8 -*-

# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import tornado

from tornado.util import bytes_type, unicode_type


class IncludeExtFiles(tornado.web.UIModule):
    def render(self):
        return ''

    def get_urls(self, file_extension):
        if hasattr(self.handler, 'ext_files'):
            ext_files = filter(
                lambda fn: '.' + file_extension in fn,
                self.handler.ext_files)
        else:
            ext_files = []

        return ext_files

    def css_files(self):
        return self.get_urls('css')

    def javascript_files(self):
        return self.get_urls('js')


class UIModuleLoader(tornado.web.UIModule):
    def __init__(self, handler):
        super().__init__(handler)
        self._resource_list = []
        self.modules = {}

    def render(self, module_class, *args, **kwargs):
        if module_class not in self.modules:
            module_instance = module_class(self.handler)
            self.modules[module_class] = module_instance

            resources = {
                'embedded_javascript':
                    module_instance.embedded_javascript(),
                'javascript_files':
                    module_instance.javascript_files(),
                'embedded_css':
                    module_instance.embedded_css(),
                'css_files':
                    module_instance.css_files(),
                'html_head':
                    module_instance.html_head(),
                'html_body':
                    module_instance.html_body(),
            }

            self._resource_list.append(resources)

        return self.modules[module_class].render(*args,
                                                 **kwargs)

    def _get_resources(self, key):
        return (r[key] for r in self._resource_list
                if key in r
                if r[key])

    def embedded_javascript(self):
        return "\n".join(self._get_resources(
            "embedded_javascript"))

    def javascript_files(self):
        result = []
        for f in self._get_resources("javascript_files"):
            if isinstance(f, (unicode_type, bytes_type)):
                result.append(f)
            else:
                result.extend(f)
        return result

    def embedded_css(self):
        return "\n".join(self._get_resources(
            "embedded_css"))

    def css_files(self):
        result = []
        for f in self._get_resources("css_files"):
            if isinstance(f, (unicode_type, bytes_type)):
                result.append(f)
            else:
                result.extend(f)
        return result

    def html_head(self):
        return "".join(self._get_resources("html_head"))

    def html_body(self):
        return "".join(self._get_resources("html_body"))
