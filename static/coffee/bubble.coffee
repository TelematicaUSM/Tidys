bubble = document.getElementById "message-bubble"
comp_style = getComputedStyle bubble
orig_tcolor = comp_style['color']
orig_bcolor = comp_style['background-color']
show_timeoutID = 0
hide_timeoutID = 0

bubble.origZIndex = parseInt(
    window.getComputedStyle(bubble)['zIndex']
)

@showBubble = (message, tcolor=orig_tcolor,
               bcolor=orig_bcolor, time=5) ->
    window.clearTimeout show_timeoutID
    window.clearTimeout hide_timeoutID
    
    bubble.style['color'] = tcolor
    bubble.style['background-color'] = bcolor
    bubble.style.transition = "none"
    bubble.innerHTML = message
    bubble.style.zIndex = bubble.origZIndex + 2
    bubble.style.opacity = 1
    show_timeoutID = window.setTimeout(hideBubble,
                                       time*1000)

@hideBubble = ->
    bubble.style.transition = "opacity 5s"
    bubble.style.opacity = 0
    hide_timeoutID = window.setTimeout ->
        bubble.style.zIndex = bubble.origZIndex
    , 5000

@showErrorBubble = (message, time=5) ->
    showBubble(message, tcolor=CONTROL_FONT_COLOR,
               bcolor=BUBBLE_ERROR_COLOR, time=time)
