#FUNCTIONS

@disconnect = ->
    ws.close()
    showHome()

@logout = ->
    delete localStorage.sessionToken
    disconnect()

sendLogout = ->
    console.log 'sendLogout not implemented!'
    return
    ws.sendSafeJSON
        'type': 'userMessage'       #database message
        'content':
            'type': 'frontendMessage'
            'content':
                'type': 'disconnect'

redirectToTeacherView = ->
    console.log 'redirectToTeacherView not implemented!'
    return

#SETUP

ws.addMessageListener 'logout', logout
ws.addMessageListener 'disconnect', disconnect

unless localStorage.sessionToken?
    showHome()

else
    #PROMISES

    @room_promise =
        if room_code?
            ws.getMessagePromise('roomCodeOk')
        else
            Promise.resolve
                'code_type': 'none'
                'room_name': null

    ustat_room_promise = Promise.all [room_promise,
        ws.getMessagePromise 'userStatus']

    #REACTIONS

    ws.addMessageListener 'tokenOk', ->
        ws.sendJSONIfOpen
            'type': 'getUserStatus'

    ustat_room_promise.then (results) ->
        room_info = results[0]
        user_status = results[1]

        distinct_room =
            room_info.room_name isnt user_status.room_name

        was_none = user_status.status is 'none'
        was_student = user_status.status is 'seat'
        was_teacher = user_status.status is 'room'

        is_none = room_info.code_type is 'none'
        is_student = room_info.code_type is 'seat'
        is_teacher = room_info.code_type is 'room'

        if distinct_room or was_student or is_student or \
           (was_none and is_teacher)
            sendLogout()
            return

        if was_teacher and is_none
            redirectToTeacherView()
            return

        if is_teacher
            load_promise.then(showLessonSetup)
        else
            load_promise.then(activatePanels)

    #RUN
    
    setHideLoadingFunction ->
    showLoading 'Preparando sesión ...'

    ws.sendJSONOnOpen
        'type': 'sessionToken',
        'token': localStorage.sessionToken

    if room_code?
        ws.sendJSONOnOpen
            'type': 'roomCode'
            'room_code': room_code
