logout_button = document.getElementById 'logout'

logout_button.addEventListener 'click', logout

ws.addEventListener ws.toEventName('tokenOk'),
    (evt) ->
        ws.sendJSON
            'type': 'getUserEMail'

ws.addEventListener ws.toEventName('userEMail'),
    (evt) ->
        document.getElementById('user-e-mail').innerHTML = \
            evt.detail.message.email
