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
    
    ws.sendJSONOnOpen
        'type': 'sessionToken',
        'token': localStorage.sessionToken

    if room_code?
        setHideLoadingFunction(->)
        
        showLoading('Localizando ...',
                    ws.getMessagePromise 'roomCodeOk')
        
        #FIXME: should send roomCode on open
        ws.addMessageListener 'tokenOk', ->
            ws.sendJSON
                'type': 'roomCode'
                'room_code': room_code
                
        ws.getMessagePromise('roomCodeOk').then (message) ->
            if message.code_type is 'room'
                load_promise.then(showLessonSetup)
            else
                load_promise.then(activatePanels)
else
    showHome()
