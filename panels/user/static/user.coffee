#VARIABLES

logout_button = document.getElementById 'logout'

#SETUP

logout_button.addEventListener 'click', logout

ws.getMessagePromise('session.start.ok').then ->
    ws.sendSafeJSON
        'type': 'getUserName'

ws.getMessagePromise('userName').then (message) ->
    document.getElementById('user-name').innerHTML = \
        message.name
