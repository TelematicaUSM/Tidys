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


#VARIABLES

remote_box = document.getElementById 'remote-control'

#FUNCION

@addNodeToRemote = (node, priority = null) ->
    new_node = document.importNode node, true
    #ver que pasa con priority null
    if priority?
        new_node.style.webkitBoxOrdinalGroup = priority
        new_node.style.mozBoxOrdinalGroup = priority
        new_node.style.boxOrdinalGroup = priority
        new_node.style.webkitOrder = priority
        new_node.style.mozOrder = priority
        new_node.style.order = priority
        new_node.style.msFlexOrder = priority
    remote_box.appendChild new_node
