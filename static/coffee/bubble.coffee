bubble = document.getElementById "message-bubble"
show_timeoutID = 0
hide_timeoutID = 0
orig_color = bubble.style.color

bubble.origZIndex = parseInt(
    window.getComputedStyle(bubble)['zIndex']
)

@showBubble = (message, color=orig_color) ->
    window.clearTimeout(show_timeoutID)
    window.clearTimeout(hide_timeoutID)
    
    bubble.style.color = color
    bubble.style.transition = "none"
    bubble.innerHTML = message
    bubble.style.zIndex = bubble.origZIndex + 2
    bubble.style.opacity = 1
    show_timeoutID = window.setTimeout(hideBubble, 5000)

@hideBubble = ->
    bubble.style.transition = "opacity 5s"
    bubble.style.opacity = 0
    hide_timeoutID = window.setTimeout ->
        bubble.style.zIndex = bubble.origZIndex
    , 5000
