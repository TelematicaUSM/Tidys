#VARIABLES

logout_button = document.getElementById 'logout'

#SETUP

logout_button.addEventListener 'click', logout

ws.getMessagePromise('tokenOk').then ->
    ws.sendJSON
        'type': 'getUserEMail'

ws.getMessagePromise('userEMail').then (message) ->
    document.getElementById('user-e-mail').innerHTML = \
        message.email
