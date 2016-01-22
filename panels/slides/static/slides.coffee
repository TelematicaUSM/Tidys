#VARIABLES

list_button_template = document.getElementById(
  'list-button-template')
t_list_button = list_button_template.content.querySelector(
  'button')

select_slide_box = document.getElementById(
  'slides-select')
spinner = document.getElementById 'slides-select-spinner'
file_input = document.getElementById 'slides-new-input'
display_template = document.querySelector(
  'template.slides.display')
display = null

current_slideshow = null
current_slide = 0

#FUNCTIONS

addButton = (slide_name, slide_id) ->
  button = document.importNode t_list_button, true
  button.textContent = slide_name
  button.addEventListener 'click', (event) ->
    ws.sendJSON
      'type': 'slides.get'
      '_id': slide_id
  select_slide_box.appendChild button

loadError = ->
  showErrorBubble(
    'Ha ocurrido un error al intentar subir el archivo!'
  )

@showSlide = (number, silent=false) ->
  ###
  Show the slide specified by `number`.

  <dl>
    <dt>Parameters</dt>
    <dd>
      <dl>
        <dt><code>number</code></dt>
        <dd>
          The number of the slide you want to show.
        </dd>

        <dt><code>silent</code></dt>
        <dd>
          Set it to `true` if you don't want errors to be
          thrown when there is no active slideshow or the
          slide number to which you want to change does not
          exist.
          Default is `false`.
        </dd>
      </dl>
    </dd>

    <dt>Raises</dt>
    <dd>
      <dl>
        <dt><code>ReferenceError</code></dt>
        <dd>
          If there is no active slideshow or the slideshow
          object does not have the <code>slides</code>
          attribute.
        </dd>

        <dt><code>RangeError</code></dt>
        <dd>
          If the slide number to which you want to change
          does not exist.
        </dd>
      </dl>
    </dd>
  </dl>
  ###
  try
    display.src = current_slideshow.slides[number].url
    current_slide = number

  catch error
    if not current_slideshow?
      if not silent
        e = new ReferenceError(
          'There is no active slideshow.')
        e.from = error
        throw e

    else if not current_slideshow.slides?
      e = new ReferenceError(
        "The slideshow object does not have the
        'slides' attribute.")
      e.from = error
      throw e

    else if number not of current_slideshow.slides
      if not silent
        e = new RangeError(
          'The slide number to which you want to
          change does not exist.')
        e.from = error
        throw e

    else
      throw error

@moveSlides = (dn, silent=false) ->
  ###
  Move `dn` slides forward.

  If `dn` is negative, then move `-dn` slides backwards from
  the current slide.

  <dl>
    <dt>Parameters</dt>
    <dd>
      <dl>
        <dt><code>dn</code></dt>
        <dd>
          The number slides to move forwards or backwards.
        </dd>

        <dt><code>silent</code></dt>
        <dd>
          Set it to `true` if you don't want errors to be
          thrown when there is no active slideshow or the
          slide number to which you want to change does not
          exist.
          Default is `false`.
        </dd>
      </dl>
    </dd>

    <dt>Raises</dt>
    <dd>
      <dl>
        <dt><code>ReferenceError</code></dt>
        <dd>
          If there is no active slideshow or the slideshow
          object does not have the <code>slides</code>
          attribute.
        </dd>

        <dt><code>RangeError</code></dt>
        <dd>
          If the slide number to which you want to change
          does not exist.
        </dd>
      </dl>
    </dd>
  </dl>
  ###
  showSlide(current_slide + dn, silent)

@prevSlide = (silent=false) ->
  ###
  Move one slide backwards.

  <dl>
    <dt>Parameters</dt>
    <dd>
      <dl>
        <dt><code>silent</code></dt>
        <dd>
          Set it to `true` if you don't want errors to be
          thrown when there is no active slideshow or the
          slide number to which you want to change does not
          exist.
          Default is `false`.
        </dd>
      </dl>
    </dd>

    <dt>Raises</dt>
    <dd>
      <dl>
        <dt><code>ReferenceError</code></dt>
        <dd>
          If there is no active slideshow or the slideshow
          object does not have the <code>slides</code>
          attribute.
        </dd>
      </dl>
      <dl>
        <dt><code>RangeError</code></dt>
        <dd>
          If the slide number to which you want to change
          does not exist.
        </dd>
      </dl>
    </dd>
  </dl>
  ###
  moveSlides(-1, silent)

@nextSlide = (silent=false) ->
  ###
  Move one slide forwards.

  <dl>
    <dt>Parameters</dt>
    <dd>
      <dl>
        <dt><code>silent</code></dt>
        <dd>
          Set it to `true` if you don't want errors to be
          thrown when there is no active slideshow or the
          slide number to which you want to change does not
          exist.
          Default is `false`.
        </dd>
      </dl>
    </dd>

    <dt>Raises</dt>
    <dd>
      <dl>
        <dt><code>ReferenceError</code></dt>
        <dd>
          If there is no active slideshow or the slideshow
          object does not have the <code>slides</code>
          attribute.
        </dd>
      </dl>
      <dl>
        <dt><code>RangeError</code></dt>
        <dd>
          If the slide number to which you want to change
          does not exist.
        </dd>
      </dl>
    </dd>
  </dl>
  ###
  moveSlides(1, silent)

#SETUP

window.addEventListener 'load', ->
  template_container = document.getElementById(
    'slides-templates')
  templates = template_container.content.querySelectorAll(
    '.template')
  addNodeToRemote?(t) for t in templates

  prev_button = document.getElementById 'slides-prev'
  next_button = document.getElementById 'slides-next'

  prev_button?.addEventListener 'click', ->
    ws.sendJSON
      'type': 'slides.prev'

  next_button?.addEventListener 'click', ->
    ws.sendJSON
      'type': 'slides.next'

ws.getMessagePromise('session.start.ok').then ->
  ws.sendJSON
    'type': 'slides.list.get'

ws.addMessageListener 'slides.list.get.ok', (message) ->
  buttons =
    document.querySelectorAll(
      '#slides-select>.list-button')

  button.remove() for button in buttons
  addButton s.name, s._id for s in message.slides

  hideElements spinner

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
  addButton message.name, message._id

ws.addMessageListener 'slides.get.ok', (message) ->
  current_slideshow = message.slide
  display = addNodeToPresentation(
    display_template.content.children[0])
  showSlide(0)
  switchToPanel 'presentation-panel'

ws.addMessageListener 'slides.prev', (message) ->
  prevSlide(silent=true)

ws.addMessageListener 'slides.next', (message) ->
  nextSlide(silent=true)
