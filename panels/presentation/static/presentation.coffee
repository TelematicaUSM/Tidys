#CODE
@addNodeToPresentation = \
    (node_template, is_main_element = true) ->
        old_node = document.importNode node_template, true
        if old_node.className ?
            if old_node.className == main-presentation-element
                if is_main_element == true
                    old_node.remove()
                    # new_node =  revisar que pasa con el nuevo nodo que debe asignarse
                else
                    old_node.className = "alt-presentation-element" #revisar si se elimina o agrega
            #else preguntar si llegara a darse esta situacion.
                #if
        else
            if is_main_element == ture
                old_node.className = main-presentation-element
            else
                old_node.className = alt-presentation-element
            document.appendChild(old_node)
