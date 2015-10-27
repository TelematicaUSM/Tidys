#VARIABLES
old_node = null
#CODE
@addNodeToPresentation = \
    (node_template, is_main_element=true) ->
        new_node = document.importNode node_template, true
        if is_main_element == true
            old_node.className = "main-presentation-element"





#classList.add'miclase'
#    .remove
#.contains
#    .toggle
