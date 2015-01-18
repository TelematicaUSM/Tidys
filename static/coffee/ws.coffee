@ws = new ReconnectingWebSocket(
    "ws://" + document.location["host"] + "/ws")
#@ws.debug = true

@ws.to_event_name = (msg_type) ->
    "msg_" + msg_type

@ws.addEventListener "message", (evt) =>
    message = JSON.parse evt.data
    
    if "type" not of message
        console.log "Malformed message: " + evt.data
        return
        
    @ws.dispatchEvent new CustomEvent(
        @ws.to_event_name(message.type),
        {"detail": "message": message})
