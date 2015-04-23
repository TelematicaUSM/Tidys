@ws = new ReconnectingWebSocket(
    "#{conf.ws_scheme}://#{document.location['host']}/ws",
    null, {debug: conf.debug, timeoutInterval: 10000})

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

ws.sendJSONIfOpen = (json_message, else_func=->) ->
    if ws.isOpen()
        ws.sendJSON json_message
    else
        else_func()

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
        console.log "Malformed message: " + evt.data
        return
        
    ws.dispatchEvent new CustomEvent(
        ws.toEventName(message.type),
        {"detail": "message": message})
)

ws.addMessageListener 'critical', (msg) ->
    showCritical msg.description
