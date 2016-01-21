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

from tornado.web import StaticFileHandler
from src.ui_methods import add_ext_file


class BoilerUIModule(tornado.web.UIModule):
    conf = {
        'static_url_prefix': '',
        'static_path': '',
        'css_files': [],
        'js_files': [],
    }

    @classmethod
    def add_handler(cls, app):
        if cls.conf['static_path'] and \
           cls.conf['static_url_prefix']:
            app.add_handlers(
                '.*$',
                [(
                    cls.conf['static_url_prefix'] + '(.*)',
                    StaticFileHandler,
                    {'path': cls.conf['static_path']}
                )]
            )

    def make_static_url(self, path):
        return StaticFileHandler.make_static_url(self.conf,
                                                 path)

    def render_string(self, path, **kwargs):
        """Render a template and returns it as a string."""
        if 'css_files' in self.conf:
            add_ext_file(
                self.handler, self.conf['css_files'],
                self.make_static_url)

        if 'js_files' in self.conf:
            add_ext_file(
                self.handler, self.conf['js_files'],
                self.make_static_url)

        return self.handler.render_string(
            path, make_static_url=self.make_static_url,
            **kwargs)
