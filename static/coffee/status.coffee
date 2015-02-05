status_text = document.getElementById 'status-panel-text'
status_panel = document.getElementById 'status-panel'

@setStatus = (message) ->
    status_text.innerHTML = message

@hideStatus = ->
    window.setTimeout ->
        status_panel.style.display = 'none'
        activate_panels()
    , 5000
