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


bubble = document.getElementById "message-bubble"
comp_style = getComputedStyle bubble
orig_tcolor = comp_style['color']
orig_bcolor = comp_style['background-color']
show_timeoutID = 0
hide_timeoutID = 0

bubble.origZIndex = parseInt(
    window.getComputedStyle(bubble)['zIndex']
)

@showBubble = (message, tcolor=orig_tcolor,
               bcolor=orig_bcolor, time=5) ->
    window.clearTimeout show_timeoutID
    window.clearTimeout hide_timeoutID

    bubble.style['color'] = tcolor
    bubble.style['background-color'] = bcolor
    bubble.style.transition = "none"
    bubble.innerHTML = message
    bubble.style.zIndex = bubble.origZIndex + 2
    bubble.style.opacity = 1
    show_timeoutID = window.setTimeout(hideBubble,
                                       time*1000)

@hideBubble = ->
    bubble.style.transition = "opacity 5s"
    bubble.style.opacity = 0
    hide_timeoutID = window.setTimeout ->
        bubble.style.zIndex = bubble.origZIndex
    , 5000

@showErrorBubble = (message, time=5) ->
    showBubble(message, tcolor=CONTROL_FONT_COLOR,
               bcolor=BUBBLE_ERROR_COLOR, time=time)
