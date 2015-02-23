main_menu_active = false;
lock_panels = false

main_menu = document.getElementById 'main-menu'
content_shade = document.getElementById 'content-shade'

main_menu_button = document.getElementById(
    'main-menu-button')

main_menu_items = document.querySelectorAll(
    '.main-menu-item')

content_shade.origZIndex = parseInt(
    window.getComputedStyle(content_shade)['zIndex'])

#FUNCTIONS

@activateMainMenu = ->
    main_menu_button.style.display = 'block'

@deactivateMainMenu = ->
    main_menu_button.style.display = 'none'

@openMainMenu = ->
    content_shade.style.zIndex =
        content_shade.origZIndex + 3
        
    content_shade.style.backgroundColor =
        'rgba(0, 0, 0, 0.6)'
        
    main_menu.style.left = '0px'
    main_menu_active = true

@closeMainMenu = ->
    content_shade.style.zIndex = content_shade.origZIndex
    content_shade.style.backgroundColor = 'transparent'
    main_menu.style.left = '-66.66666vw'
    main_menu_active = false

@switchMainMenu = ->
    if main_menu_active
        closeMainMenu()
    else
        openMainMenu()

@lockPanels = ->
    lock_panels = true

@unlockPanels = ->
    lock_panels = false

@hideAllPanels = ->
    return if lock_panels
    
    for panel in document.querySelectorAll(
            ".panel, .scrolling-panel, .fixed-panel")
        panel.style.display = "none"

@switchToPanel = (panel_id) ->
    return if lock_panels
    
    panel = document.getElementById(panel_id)
    
    if 'locking_panel' in panel.classList
        deactivatePanels()
    else
        activateMainMenu()
        hideAllPanels()
        closeMainMenu()
    
    panel.style.display = "block"
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0

@getPanelSwitch = (panel_id) -> ->
    switchToPanel panel_id

@activatePanels = ->
    return if lock_panels
    activateMainMenu()
    switchToPanel main_menu_items[0].dataset.panelId

@deactivatePanels = ->
    return if lock_panels
    deactivateMainMenu()
    hideAllPanels()

#SETUP

document.getElementById('main-menu-button'). \
    addEventListener 'click', switchMainMenu
content_shade.addEventListener 'click', closeMainMenu

for button in main_menu_items
    button.addEventListener('click',
        getPanelSwitch button.dataset.panelId)
