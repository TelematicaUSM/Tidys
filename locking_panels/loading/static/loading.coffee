loading_text = document.getElementById 'loading-text'
promise_num = 0

check_promise_num = ->
    if promise_num < 0
        throw new RangeError("The number of promises
                              registered in this module
                              cannot be negative!")

origHideLoadingFunction = ->
    activatePanels()

hideLoading = origHideLoadingFunction

resolve_promise = ->
    promise_num--
    check_promise_num()
    hideLoading() unless promise_num

add_promise = (promise) ->
    promise.then resolve_promise, resolve_promise
    promise_num++
    check_promise_num()

@showLoading = (message='Loading ...', promise=null,
                min_time=5000) ->
    unless promise_num
        switchToPanel('loading-panel')
        add_promise(
            new Promise(
                (resolve, reject) ->
                    setTimeout resolve, min_time
            )
        )
    
    add_promise promise if promise
    loading_text.innerHTML = message

@setHideLoadingFunction = (func) ->
    hideLoading = func

@resetHideLoadingFunction = ->
    hideLoading = origHideLoadingFunction
