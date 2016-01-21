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


@getEventPromise = (target, type, pre_check = false) ->
    listener = undefined

    promise = new Promise (resolve, reject) ->
        if pre_check
            resolve()
        else
            listener = resolve
            target.addEventListener type, listener

    unless pre_check
        promise.then ->
            target.removeEventListener type, listener

    return promise

@ensureArray = (object) ->
    return object if Array.isArray object
    return [object]

@hideElements = (elements) ->
    elements = ensureArray elements
    element.style.display = 'none' for element in elements

@showElements = (elements, display = 'block') ->
    elements = ensureArray elements
    element.style.display = display for element in elements

# This name should be changed to switchElementsVisibility
@switchElements_visibility = \
        (elements, display = 'block') ->
    elements = ensureArray elements
    for element in elements
        if element.style.display is 'none'
            showElement element, display
        else
            hideElement element
