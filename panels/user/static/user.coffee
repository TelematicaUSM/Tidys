#VARIABLES

logout_button = document.getElementById 'logout'

#SETUP

logout_button.addEventListener 'click', logout

ws.getMessagePromise('tokenOk').then ->
    showLoading('Obteniendo nombre de usuario ...',
                ws.getMessagePromise 'userName')
    ws.sendSafeJSON
        'type': 'getUserName'

ws.getMessagePromise('userName').then (message) ->
    document.getElementById('user-name').innerHTML = \
        message.name
