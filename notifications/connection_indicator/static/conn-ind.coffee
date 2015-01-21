path = document.querySelector('#conn-ind path');

path.origFill = window.getComputedStyle(path)['fill']

ws.addEventListener "open", (evt) ->
    path.style.fill = '#414141'

ws.addEventListener "close", (evt) ->
    path.style.fill = path.origFill

document.querySelector('#conn-ind').addEventListener(
    "click", (evt) ->
        if ws.readyState == WebSocket.OPEN
            show_bubble "Conectado."
        else
            show_bubble "Sin conexión. Verifique que " +
                        "tenga acceso a internet.")
