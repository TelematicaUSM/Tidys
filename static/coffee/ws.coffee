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


@ws = new ReconnectingWebSocket(
    "#{conf.ws_scheme}://#{document.location['host']}/ws",
    null,
    {
        debug: conf.debug,
        timeoutInterval: 10000,
        reconnectInterval: \
            conf.ws_reconnect_interval * 1000,
    }
)

ws.promises = {}
open_promise = undefined

#FUNCTIONS

ws.isOpen = ->
    ws.readyState == ReconnectingWebSocket.OPEN

ws.getOpenPromise = ->
    if open_promise?
        open_promise
    else
        open_promise = getEventPromise(
            ws, 'open', ws.isOpen()
        )

ws.toEventName = (msg_type) ->
    "msg_" + msg_type

ws.sendJSON = (json_message) ->
    ws.send JSON.stringify json_message

ws.sendJSONIfOpen = (json_message, else_func = ->) ->
    if ws.isOpen()
        ws.sendJSON json_message
    else
        else_func()

ws.sendJSONOnOpen = (json_message) ->
    #Send JSON now and on every open event.
    ws.sendJSONIfOpen json_message
    ws.addEventListener 'open', ->
        ws.sendJSON json_message

ws.sendSafeJSON = (json_message) ->
    ws.sendJSONIfOpen json_message, ->
        ws.getOpenPromise().then ->
            ws.sendJSON json_message

ws.addMessageListener = (msg_type, func) ->
    listener = (evt) ->
        func evt.detail.message
    listener.msg_type = msg_type

    ws.addEventListener ws.toEventName(msg_type), listener
    return listener

ws.removeMessageListener = (listener) ->
    ws.removeEventListener(
        ws.toEventName(listener.msg_type), listener)

ws.getMessagePromise = (msg_type) ->
    unless msg_type of ws.promises
        listener = undefined
        ws.promises[msg_type] = \
            new Promise (resolve, reject) ->
                listener = ws.addMessageListener(msg_type,
                                                 resolve)
        ws.promises[msg_type].then ->
            ws.removeMessageListener listener
    ws.promises[msg_type]

#SETUP

showLoading('Conectando con el servidor WebSocket ...',
            ws.getOpenPromise())

ws.addEventListener 'close', ->
    open_promise = undefined

ws.addEventListener("message", (evt) ->
    message = JSON.parse evt.data

    if "type" not of message
        throw new Error "Malformed message: " + evt.data

    ws.dispatchEvent new CustomEvent(
        ws.toEventName(message.type),
        {"detail": "message": message})
)

ws.addMessageListener 'critical', (msg) ->
    showCritical msg.description
