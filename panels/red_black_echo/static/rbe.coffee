ws.addEventListener ws.toEventName('white'), (evt) ->
    document.getElementById('result').value +=
        evt.detail.message.string + '\n'

send = (color) ->
    msg = {
        'type': color,
        'string': document.getElementById(color).value
    }
    
    ws.sendJSON msg

document.getElementById('red-button').addEventListener(
    'click', -> send 'red')

document.getElementById('black-button').addEventListener(
    'click', -> send 'black')
