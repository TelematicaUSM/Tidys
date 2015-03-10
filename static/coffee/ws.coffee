@ws = new ReconnectingWebSocket(
    "#{conf.ws_scheme}://#{document.location['host']}/ws",
    null, {debug: conf.debug, timeoutInterval: 10000})

ws.open_promise = new Promise (resolve, reject) ->
    if ws.readyState == ReconnectingWebSocket.OPEN
        resolve()
    else
        ws.addEventListener "open", resolve

ws.promises = {}

#FUNCTIONS

ws.toEventName = (msg_type) ->
    "msg_" + msg_type

ws.sendJSON = (json_message) ->
    ws.send JSON.stringify json_message

ws.addMessageListener = (msg_type, func) ->
    ws.addEventListener ws.toEventName(msg_type), (evt) ->
        func evt.detail.message

ws.getMessagePromise = (msg_type) ->
    unless msg_type of ws.promises
        ws.promises[msg_type] = \
            new Promise (resolve, reject) ->
                ws.addMessageListener msg_type, resolve
    ws.promises[msg_type]

#SETUP

showLoading('Conectando con el servidor WebSocket ...',
            ws.open_promise)

ws.addEventListener("message", (evt) ->
    message = JSON.parse evt.data
    
    if "type" not of message
        console.log "Malformed message: " + evt.data
        return
        
    ws.dispatchEvent new CustomEvent(
        ws.toEventName(message.type),
        {"detail": "message": message})
)
