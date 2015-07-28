#FUNCTIONS

@disconnect = ->
    ws.close()
    showHome()

@logout = ->
    delete localStorage.sessionToken
    disconnect()

@replaceLocation = (message) ->
    document.location.replace message.url

#SETUP

ws.addMessageListener 'logout', logout
ws.addMessageListener 'disconnect', disconnect
ws.addMessageListener 'replaceLocation', replaceLocation

ws.getMessagePromise('session.start.ok').then (message) ->
    if message.code_type == 'room' and \
            message.course_id == null
        load_promise.then showLessonSetup
    else
        load_promise.then activatePanels

unless localStorage.sessionToken?
    disconnect()

else
    setHideLoadingFunction ->
    showLoading 'Preparando sesión ...'

    ws.sendJSONOnOpen
        'type': 'session.start',
        'token': localStorage.sessionToken
        'room_code': if room_code? then room_code \
                     else 'none'
