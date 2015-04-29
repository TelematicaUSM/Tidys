#VARIABLES

panel_id = 'lesson-setup-panel'
panel = document.getElementById panel_id

#FUNCTIONS

@showLessonSetup = ->
    switchToPanel(panel_id)

#SETUP
#FIXME: should wait for userok, not for roomCoseOk
ws.getMessagePromise('roomCodeOk').then ->
    ws.sendSafeJSON
        'type': 'getCourses'

ws.getMessagePromise('courses').then ->
    console.log 'Dejo la patá!'
