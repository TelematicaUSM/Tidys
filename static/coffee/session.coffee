#FUNCTIONS

@logout = ->
    delete localStorage.sessionToken
    ws.close()
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

    if room_code?
        ws.addMessageListener 'tokenOk', ->
            ws.sendJSON
                'type': 'roomCode'
                'room_code': room_code
        
        ws.addMessageListener 'roomCodeOk', ->
else
    showHome()
