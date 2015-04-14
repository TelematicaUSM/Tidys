#FUNCTIONS

@logout = ->
    delete localStorage.sessionToken
    showHome()

#SETUP

ws.addMessageListener 'logout', logout

if localStorage.sessionToken?
    showLoading('Autenticando ...',
                ws.getMessagePromise 'tokenOk')

    ws.open_promise.then ->
        ws.sendJSON
            'type': 'sessionToken'
            'token': localStorage.sessionToken
else
    showHome()

ws.getMessagePromise('tokenOk').then ->
    ws.sendJSON
        'type': 'roomCode'
        'room_code': room_code

ws.addMessageListener 'roomOk', ()->return
