#VARIABLES
remote_box = document.getElementById 'remote-control'
#FUNCION
@addNodeToRemote = (node, priority = null) ->
    new_node = document.importNode node, true
    #ver que pasa con priority null
    if priority?
        new_node.style.webkitBoxOrdinalGroup = priority
        new_node.style.mozBoxOrdinalGroup = priority
        new_node.style.boxOrdinalGroup = priority
        new_node.style.webkitOrder = priority
        new_node.style.mozOrder = priority
        new_node.style.order = priority
        new_node.style.msFlexOrder = priority
    remote_box.appendChild new_node
