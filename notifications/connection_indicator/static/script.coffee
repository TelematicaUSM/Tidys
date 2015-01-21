path = document.querySelector('#conn-ind path');

ws.addEventListener "open", (evt) ->
    path.style.fill = '#414141'

ws.addEventListener "close", (evt) ->
    path.style.fill = 'rgba(65, 65, 65, 0.15)'

document.querySelector('#conn-ind').addEventListener(
    "click", (evt) ->
        ws.refresh() \
        if not ws.readyState = WebSocket.CLOSED)
