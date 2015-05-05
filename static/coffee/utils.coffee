@getEventPromise = (target, type, pre_check=false) ->
    listener = undefined
    
    promise = new Promise (resolve, reject) ->
        if pre_check
            resolve()
        else
            listener = resolve
            target.addEventListener type, listener
    
    unless pre_check
        promise.then ->
            target.removeEventListener type, listener
        
    return promise

@ensureArray = (object) ->
    return object if Array.isArray object
    return [object]

@hideElements = (elements) ->
    elements = ensureArray elements
    element.style.display = 'none' for element in elements

@showElements = (elements, display='block') ->
    elements = ensureArray elements
    element.style.display = display for element in elements

@switchElements_visibility = (elements, display='block') ->
    elements = ensureArray elements
    for element in elements
        if element.style.display is 'none'
            showElement element, display
        else
            hideElement element
