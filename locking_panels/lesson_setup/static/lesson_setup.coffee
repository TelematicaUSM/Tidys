loading_text = document.getElementById 'loading-text'
promise_num = 0
@load_promise = null
resolveLoadPromise = null

origHideLoadingFunction = ->
    activatePanels()

hideLoading = origHideLoadingFunction

checkPromiseNum = ->
    if promise_num < 0
        throw new RangeError("The number of promises
                              registered in this module
                              cannot be negative!")

resolvePromise = =>
    promise_num--
    checkPromiseNum()
    unless promise_num
        resolveLoadPromise()
        @load_promise = null
        resolveLoadPromise = null

addPromise = (promise) ->
    promise.then resolvePromise, resolvePromise
    promise_num++
    checkPromiseNum()

@showLoading = (message='Loading ...', promise=null,
                min_time=5000) =>
    unless promise_num
        switchToPanel('loading-panel')
        addPromise(
            new Promise(
                (resolve, reject) ->
                    setTimeout resolve, min_time
            )
        )
        @load_promise = new Promise(
            (resolve, reject) ->
                resolveLoadPromise = resolve
        )
        @load_promise.then(hideLoading)
    
    addPromise promise if promise
    loading_text.innerHTML = message

@setHideLoadingFunction = (func) ->
    hideLoading = func

@resetHideLoadingFunction = ->
    hideLoading = origHideLoadingFunction
