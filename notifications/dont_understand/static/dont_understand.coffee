DURATION = 1 * 60

@d_understand = document.getElementById 'dont-understand'
du_icon = document.querySelector '#dont-understand g'

# FUNCTIONS

d_understand.start = ->
    if ws.isOpen()
        this.classList.add 'animated'
        this.timeoutID = setTimeout(
            ->
                d_understand.classList.remove 'animated'
            ,
            DURATION*1000
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

ws.getMessagePromise('course.assignment.ok').then ->
    d_understand.style.display = 'block'

ws.getMessagePromise('studentSetup.course.set.ok').then ->
    d_understand.style.display = 'block'
    d_understand.addEventListener(
        'click', d_understand.toggle)

ws.addMessageListener(
    'dontUnderstand.icon.state.set',
    (message) ->
        c = tinycolor.mix(
            ICON_COLOR, PRIMARY_COLOR,
            message.proportion*100)
        du_icon.style.fill = c.toHexString()
)
