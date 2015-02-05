bubble = document.getElementById "message-bubble"
show_timeoutID = 0
hide_timeoutID = 0

bubble.origZIndex = parseInt(
    window.getComputedStyle(bubble)['zIndex']
)

@show_bubble = (message) ->
    window.clearTimeout(show_timeoutID)
    window.clearTimeout(hide_timeoutID)
    
    bubble.style.transition = "none"
    bubble.innerHTML = message
    bubble.style.zIndex = bubble.origZIndex + 2
    bubble.style.opacity = 1
    show_timeoutID = window.setTimeout(hide_bubble, 5000)

@hide_bubble = ->
    bubble.style.transition = "opacity 5s"
    bubble.style.opacity = 0
    hide_timeoutID = window.setTimeout ->
        bubble.style.zIndex = bubble.origZIndex
    , 5000
