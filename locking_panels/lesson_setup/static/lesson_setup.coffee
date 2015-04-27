#VARIABLES

panel_id = 'lesson-setup-panel'
panel = document.getElementById panel_id

#FUNCTIONS

@showLessonSetup = ->
    switchToPanel(panel_id)

#SETUP

ws.getMessagePromise('tokenOk').then ->
    showLoading('Obteniendo nombre de usuario ...',
                ws.getMessagePromise 'userName')
    ws.sendSafeJSON
        'type': 'getUserName'

ws.getMessagePromise('userName').then (message) ->
    document.getElementById('user-name').innerHTML = \
        message.name
