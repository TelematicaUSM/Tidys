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

current_node = null
fs_button = document.getElementById 'presentation-box-fullscreen'
ufs_button = document.getElementById 'presentation-box-unfullscreen'
presentation_box = document.getElementById 'presentation-box'
#FUNCIONES

@addNodeToPresentation = \
  (node_template, is_main_element = true) ->
    try
      new_node = document.importNode node_template, true

      if is_main_element == true
        current_node?.remove()
        new_node.classList.add 'main-presentation-element'
        current_node = new_node

      else
        new_node.classList.add 'alt-presentation-element'
      presentation_box.appendChild new_node
      fs_button.style.display = "block"
      return new_node

    catch error
      unless node_template instanceof Node
        e = TypeError(
          'La variable node_template no es un Nodo HTML.')
        e.from = error
        throw e

      else
        throw error

updateFullScreenIcon = () ->
  if document.fullscreenElement or \
      document.mozFullScreenElement
    hideElements fs_button
    showElements ufs_button
  else
    hideElements ufs_button
    showElements fs_button

fullscreenClick = () ->
  if current_node?.requestFullscreen?
    presentation_box.requestFullscreen()

  else if current_node?.msRequestFullscreen?
    presentation_box.msRequestFullscreen()

  else if current_node?.mozRequestFullScreen?
    presentation_box.mozRequestFullScreen()

  else if current_node?.webkitRequestFullscreen?
    presentation_box.webkitRequestFullscreen()

unfullscreenClick = () ->
  # document.mozCancelFullscreen()
  if document.exitFullscreen?
    document.exitFullscreen()

  else if document.msExitFullscreen?
    document.msExitFullscreen()

  else if document.mozCancelFullScreen?
    document.mozCancelFullScreen()

  else if document.webkitExitFullscreen?
    document.webkitExitFullscreen()

#SETUP
fs_button.addEventListener 'click', fullscreenClick
#unless presentation_box.mozFullScreenEnabled
  #showElements(fs_button)
ufs_button.addEventListener 'click', unfullscreenClick
#if presentation_box.mozFullScreenEnabled
#  showElements(ufs_button)
full_screen_events = [
  'webkitfullscreenchange', 'mozfullscreenchange',
  'fullscreenchange', 'MSFullscreenChange']

for event in full_screen_events
  document.addEventListener event, updateFullScreenIcon




  document.addEventListener
