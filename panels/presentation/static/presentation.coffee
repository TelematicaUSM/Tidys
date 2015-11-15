#VARIABLES

old_node = null

#FUNCIONES

@addNodeToPresentation = \
    (node_template, is_main_element = true) ->
        new_node = document.importNode node_template, true

        unless new_node.classList?
            throw 'reemplazar una excepcion aqui'

        if is_main_element == true
            old_node.remove() if old_node?
            new_node.classList.add(
                'main-presentation-element')
            old_node = new_node
        else
            new_node.classList.add(
                'alt-presentation-element')
        panel= document.getElementById('presentation-panel')
        panel.appendChild(new_node)

#SETUP

document.querySelector(
    '#presentation-panel > h1:nth-child(1)').remove()
