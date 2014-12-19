var main_menu_active = false;
var main_menu = document.getElementById("main-menu");
var content_shade = document.getElementById(
    "content-shade");
    
content_shade.origZIndex = parseInt(
    window.getComputedStyle(content_shade)['zIndex']);

function open_main_menu() {
    content_shade.style.zIndex =
        content_shade.origZIndex + 2;
        
    content_shade.style.backgroundColor =
        "rgba(0, 0, 0, 0.6)";
        
    main_menu.style.left = "0px";
    main_menu_active = true;
}

function close_main_menu() {
    content_shade.style.zIndex = content_shade.origZIndex;
    content_shade.style.backgroundColor = "transparent";
    main_menu.style.left = "-66.66666vw";
    main_menu_active = false;
}

function switch_main_menu() {
    if (main_menu_active)
        close_main_menu();
    else
        open_main_menu();
}

function switchToPanel(panel_id) {
    var panels = document.querySelectorAll(".panel")
    var i;
    for (i=0; i<panels.length; i++)
        panels[i].style.display = "none";
    
    document.getElementById(panel_id).style.display =
        "block";
    
    close_main_menu();
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
