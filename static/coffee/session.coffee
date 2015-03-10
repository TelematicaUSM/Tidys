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
