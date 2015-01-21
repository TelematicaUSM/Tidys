main_menu_active = false;
main_menu = document.getElementById "main-menu"
content_shade = document.getElementById "content-shade"
    
content_shade.origZIndex = parseInt(
    window.getComputedStyle(content_shade)['zIndex']
)

@open_main_menu = () ->
    content_shade.style.zIndex =
        content_shade.origZIndex + 3
        
    content_shade.style.backgroundColor =
        "rgba(0, 0, 0, 0.6)"
        
    main_menu.style.left = "0px"
    main_menu_active = true

@close_main_menu = ->
    content_shade.style.zIndex = content_shade.origZIndex
    content_shade.style.backgroundColor = "transparent"
    main_menu.style.left = "-66.66666vw"
    main_menu_active = false

@switch_main_menu = ->
    if main_menu_active
        close_main_menu()
    else
        open_main_menu()

@switchToPanel = (panel_id) -> ->
    for panel in document.querySelectorAll ".panel"
        panel.style.display = "none"
    
    document.getElementById(panel_id).style.display =
        "block"
    
    close_main_menu()
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0

document.getElementById("main-menu-button"). \
    addEventListener "click", @switch_main_menu

content_shade.addEventListener "click", @close_main_menu

for button in document.querySelectorAll ".main-menu-item"
    button.addEventListener("click",
        @switchToPanel button.dataset.panelId)
