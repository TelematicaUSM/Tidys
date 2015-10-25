@d_understand = document.getElementById 'dont-understand'

# FUNCTIONS

d_understand.start = ->
    if ws.isOpen()
        this.classList.add 'animated'
        this.timeoutID = setTimeout(
            ->
                d_understand.stop()
            ,
            1*60*1000
        )
        ws.sendJSON
            type: 'dontUnderstand.start'

d_understand.stop = ->
    if ws.isOpen()
        this.classList.remove 'animated'
        clearTimeout(this.timeoutID)
        ws.sendJSON
            type: 'dontUnderstand.stop'

d_understand.toggle = ->
    if this.classList.contains 'animated'
        this.stop()
    else
        this.start()

# SETUP

d_understand.addEventListener 'click', d_understand.toggle
