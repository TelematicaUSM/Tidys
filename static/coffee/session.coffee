#FUNCTIONS

@logout = ->
    delete localStorage.sessionToken
    showHome()

token_message =
    'type': 'sessionToken',
    'token': localStorage.sessionToken

#SETUP

ws.addMessageListener 'logout', logout

if localStorage.sessionToken?
    showLoading('Autenticando ...',
                ws.getMessagePromise 'tokenOk')
    
    ws.sendJSONIfOpen token_message
    ws.addEventListener 'open', ->
        ws.sendJSON token_message
else
    showHome()

ws.addMessageListener 'tokenOk', ->
    if room_code?
        ws.sendJSON
            'type': 'roomCode'
            'room_code': room_code
