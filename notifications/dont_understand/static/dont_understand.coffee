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


DURATION = 1 * 60

@d_understand = document.getElementById 'dont-understand'
du_icon = document.querySelector '#dont-understand g'

# FUNCTIONS

d_understand.start = ->
    if ws.isOpen()
        this.classList.add 'animated'
        this.timeoutID = setTimeout(
            ->
                d_understand.classList.remove 'animated'
            ,
            DURATION*1000
        )
        ws.sendJSON
            type: 'dontUnderstand.start'

d_understand.stop = ->
    if ws.isOpen()
        this.classList.remove 'animated'
        clearTimeout(this.timeoutID)
        ws.sendJSON
            type: 'dontUnderstand.stop'

d_understand.toggle = ->
    if this.classList.contains 'animated'
        this.stop()
    else
        this.start()

# SETUP

ws.getMessagePromise('course.assignment.ok').then ->
    d_understand.style.display = 'block'

ws.getMessagePromise('studentSetup.course.set.ok').then ->
    d_understand.style.display = 'block'
    d_understand.addEventListener(
        'click', d_understand.toggle)

ws.addMessageListener(
    'dontUnderstand.icon.state.set',
    (message) ->
        c = tinycolor.mix(
            ICON_COLOR, PRIMARY_COLOR,
            message.proportion*100)
        du_icon.style.fill = c.toHexString()
)
