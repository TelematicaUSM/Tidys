@ws.addEventListener @ws.to_event_name("white"), (evt) ->
    document.getElementById("result").value +=
        evt.detail.message.string + '\n'

send = (color) =>
    msg = {
        "type": color,
        "string": document.getElementById(color).value
    }
    
    @ws.send JSON.stringify msg

document.getElementById("red-button").addEventListener(
    "click", -> send "red")

document.getElementById("black-button").addEventListener(
    "click", -> send "black")
