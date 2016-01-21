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


import src


class RemotePanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'remote-panel'
    classes = {'scrolling-panel', 'teacher'}
    name = 'Control Remoto'
    conf = {
        'static_url_prefix': '/remote/',
        'static_path': './panels/remote/static',
        'css_files': ['remote.css'],
        'js_files': ['remote.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/remote/remote.html')
