loading_text = document.getElementById 'loading-text'
promise_num = 0
@load_promise = null
resolve_load_promise = null

checkPromiseNum = ->
    if promise_num < 0
        throw new RangeError("The number of promises
                              registered in this module
                              cannot be negative!")

origHideLoadingFunction = ->
    activatePanels()

hideLoading = origHideLoadingFunction

resolvePromise = ->
    promise_num--
    checkPromiseNum()
    unless promise_num
        hideLoading()
        resolve_load_promise()
        load_promise = null
        resolve_load_promise = null

addPromise = (promise) ->
    promise.then resolvePromise, resolvePromise
    promise_num++
    checkPromiseNum()

@showLoading = (message='Loading ...', promise=null,
                min_time=5000) ->
    unless promise_num
        switchToPanel('loading-panel')
        addPromise(
            new Promise(
                (resolve, reject) ->
                    setTimeout resolve, min_time
            )
        )
        load_promise = new Promise(
            (resolve, reject) ->
                resolve_load_promise = resolve
        )
    
    addPromise promise if promise
    loading_text.innerHTML = message

@setHideLoadingFunction = (func) ->
    hideLoading = func

@resetHideLoadingFunction = ->
    hideLoading = origHideLoadingFunction
