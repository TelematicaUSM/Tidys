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


#FUNCTIONS

@disconnect = ->
    ws.close()
    showHome()

@logout = ->
  delete localStorage.sessionToken
  disconnect()

@replaceLocation = (message) ->
  document.location.replace message.url

#SETUP

ws.addMessageListener 'logout', logout
ws.addMessageListener 'disconnect', disconnect
ws.addMessageListener 'replaceLocation', replaceLocation

ws.getMessagePromise('session.start.ok').then (message) ->
  @user =
      status: message.code_type

  if message.code_type == 'room' and \
      message.course_id == null
    load_promise.then showLessonSetup

  else if message.code_type == 'seat'
    load_promise.then showStudentSetup

  else
    load_promise.then activatePanels

unless localStorage.sessionToken?
  disconnect()

else
  setHideLoadingFunction ->
  showLoading 'Preparando sesión ...'

  ws.sendJSONOnOpen
    'type': 'session.start',
    'token': localStorage.sessionToken
    'room_code': if room_code? then room_code \
                 else 'none'
