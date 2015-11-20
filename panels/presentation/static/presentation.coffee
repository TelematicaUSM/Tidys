#VARIABLES

current_node = null
fs_button = document.getElementById "presentation-box-fullscreen"
presentation_box = document.getElementById "presentation-box"
#FUNCIONES

@addNodeToPresentation = \
    (node_template, is_main_element = true) ->
        new_node = document.importNode node_template, true

        unless new_node.classList?
            throw 'reemplazar una excepcion aqui'

        if is_main_element == true
            current_node.remove() if current_node?
            new_node.classList.add(
                'main-presentation-element')
            current_node = new_node
        else
            new_node.classList.add('alt-presentation-element')
        presentation_box.appendChild(new_node)
        fs_button.style.display = "block"



fullscreenClick = () ->
    if current_node?.requestFullscreen?
        current_node.requestFullscreen()
    else if current_node?.msRequestFullscreen?
        current_node.msRequestFullscreen()
    else if current_node?.mozRequestFullScreen?
        current_node.mozRequestFullScreen()
    else if current_node?.webkitRequestFullscreen?
        current_node.webkitRequestFullscreen()


#SETUP
fs_button.addEventListener 'click', fullscreenClick
