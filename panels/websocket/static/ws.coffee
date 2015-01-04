@ws.addEventListener "message", (evt) ->
    document.getElementById("result").value +=
        evt.data + '\n'

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
