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


class LoadingLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    id_ = 'loading-panel'
    classes = {'scrolling-panel', 'system'}
    conf = {
        'static_url_prefix': '/loading/',
        'static_path': './locking_panels/loading/static',
        'css_files': ['loading.css'],
        'js_files': [],
    }

    def render(self):
        return self.render_string(
            '../locking_panels/loading/loading.html')
