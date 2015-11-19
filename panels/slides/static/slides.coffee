#VARIABLES

template = document.getElementById 'list-button-template'
tbutton = template.content.querySelector 'button'
select_slide_box = document.getElementById(
    'select-slide-box')
spinner = document.getElementById 'select-slide-spinner'
file_input = document.getElementById 'slide-file-input'

#FUNCIONES

addButton = (slide_name, slide_id) ->
    button = document.importNode(tbutton, true)
    button.textContent = slide_name
    button.slide_id = slide_id
    button.addEventListener 'click', (event) ->
        launchSlideShow(event.target.slide_id)
    select_slide_box.appendChild button

launchSlideShow = ->
    throw new Error('Not implemented!')

loadError = ->
    showErrorBubble(
        'Ha ocurrido un error al intentar subir el archivo!'
    )

#SETUP

ws.getMessagePromise('session.start.ok').then ->
    ws.sendJSON
        'type': 'slides.list.get'

ws.addMessageListener 'slides', (message) ->
    button.remove() for button in document.querySelectorAll(
        '#select-slide-box>.list-button')

    addButton s.name, s._id for s in message.slides

    hideElements spinner

    if message.slides.length is 0
        hideElements select_slide_box
    else
        showElements select_slide_box

file_input.addEventListener 'change', ->
    file = file_input.files[0]
    fr = new FileReader()

    fr.onload = ->
        buffer = new Uint8Array(fr.result)
        ws.sendJSONIfOpen(
            {
                'type': 'slides.add'
                'mime': file.type
                'data': Unibabel.bufferToBase64(buffer)
            }
        )

    fr.onerror = loadError
    fr.readAsArrayBuffer file

ws.addMessageListener 'slides.add.ok', (message) ->
