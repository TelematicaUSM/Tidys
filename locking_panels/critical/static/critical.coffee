panel_id = 'critical-panel'
critical_panel = document.getElementById panel_id
critical_text = document.getElementById 'critical-text'

@showCritical = (message='Error!') ->
    critical_text.innerHTML = message
    switchToPanel(panel_id)
    lockPanels()
