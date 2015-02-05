@logout = ->
    delete localStorage.sessionToken
    document.location.replace('/login')

if not localStorage.sessionToken?
    setStatus 'Redireccionando a login con google en 5
                segundos ...'
    setTimeout ->
        document.location.replace('/login')
    , 5000
else
    ws.addEventListener ws.toEventName('logout'),
        (evt) ->
            logout()
            
    ws.addEventListener ws.toEventName('tokenOk'),
        (evt) ->
            hideStatus()

    ws.addEventListener "open", (evt) ->
        ws.sendJSON 
            'type': 'sessionToken'
            'token': localStorage.sessionToken
