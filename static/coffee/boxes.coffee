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


main_menu_active = false
lock_panels = false

main_menu = document.getElementById 'main-menu'
content_shade = document.getElementById 'content-shade'

main_menu_button = document.getElementById(
  'main-menu-button')

main_menu_items = document.querySelectorAll(
  '.main-menu-item')

content_shade.origZIndex = parseInt(
  window.getComputedStyle(content_shade)['zIndex'])

@active_panel = null

#FUNCTIONS

@activateMainMenu = ->
  main_menu_button.style.display = 'block'

@deactivateMainMenu = ->
  main_menu_button.style.display = 'none'

@openMainMenu = ->
  content_shade.style.zIndex =
    content_shade.origZIndex + 3

  content_shade.style.backgroundColor =
    'rgba(0, 0, 0, 0.6)'

  main_menu.style.left = '0px'
  main_menu_active = true

@closeMainMenu = ->
  content_shade.style.zIndex = content_shade.origZIndex
  content_shade.style.backgroundColor = 'transparent'
  main_menu.style.left = '-66.66666vw'
  main_menu_active = false

@switchMainMenu = ->
  if main_menu_active
    closeMainMenu()
  else
    openMainMenu()

@lockPanels = ->
  lock_panels = true

@unlockPanels = ->
  lock_panels = false

@hideAllPanels = ->
  return if lock_panels

  for panel in document.querySelectorAll(
    ".panel, .scrolling-panel, .fixed-panel")
    panel.style.display = "none"
  @active_panel = null

@switchToPanel = (panel_id) ->
  return if lock_panels

  panel = document.getElementById(panel_id)

  if 'locking_panel' in panel.classList
    deactivatePanels()
  else
    activateMainMenu()
    hideAllPanels()
    closeMainMenu()

  panel.style.display = "block"
  document.body.scrollTop = 0
  document.documentElement.scrollTop = 0
  @active_panel = panel_id

@getPanelSwitch = (panel_id) -> ->
  switchToPanel panel_id

@activatePanels = ->
  return if lock_panels
  if main_menu_items[0]?
    switchToPanel main_menu_items[0].dataset.panelId
  else
    activateMainMenu()
    hideAllPanels()

@deactivatePanels = ->
  return if lock_panels
  deactivateMainMenu()
  hideAllPanels()

#SETUP

document.getElementById('main-menu-button'). \
  addEventListener 'click', switchMainMenu
content_shade.addEventListener 'click', closeMainMenu

for button in main_menu_items
  button.addEventListener('click',
    getPanelSwitch button.dataset.panelId)
