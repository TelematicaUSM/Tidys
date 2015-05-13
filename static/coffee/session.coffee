#FUNCTIONS

@logout = ->
    delete localStorage.sessionToken
    ws.close()
    showHome()

localizationSetup = ->
    setHideLoadingFunction ->
    
    showLoading('Localizando ...',
                ws.getMessagePromise 'roomCodeOk')
    
    ws.sendJSONOnOpen
        'type': 'roomCode'
        'room_code': room_code
            
    ws.getMessagePromise('roomCodeOk').then (message) ->
        if message.code_type is 'room'
            load_promise.then(showLessonSetup)
        else
            load_promise.then(activatePanels)

#SETUP

ws.addMessageListener 'logout', logout

if localStorage.sessionToken?
    showLoading('Autenticando ...',
                ws.getMessagePromise 'tokenOk')
    
    ws.sendJSONOnOpen
        'type': 'sessionToken',
        'token': localStorage.sessionToken

    #averiguar si el usuario estaba haciendo algo con
    #anterioridad

    if room_code?
        localizationSetup()
else
    showHome()
