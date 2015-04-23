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
