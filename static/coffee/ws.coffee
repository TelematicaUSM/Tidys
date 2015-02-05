@ws = new ReconnectingWebSocket(
    "#{conf.ws_scheme}://#{document.location['host']}/ws",
    null, {debug: conf.debug})

#FUNCTIONS

ws.toEventName = (msg_type) ->
    "msg_" + msg_type

ws.sendJSON = (json_message) ->
    ws.send JSON.stringify json_message

#SETUP

ws.addEventListener("message", (evt) ->
    message = JSON.parse evt.data
    
    if "type" not of message
        console.log "Malformed message: " + evt.data
        return
        
    ws.dispatchEvent new CustomEvent(
        ws.toEventName(message.type),
        {"detail": "message": message})
)
