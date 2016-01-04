#VARIABLES

current_node = null
fs_button = document.getElementById 'presentation-box-fullscreen'
ufs_button = document.getElementById 'presentation-box-unfullscreen'
presentation_box = document.getElementById 'presentation-box'
#FUNCIONES

@addNodeToPresentation = \
  (node_template, is_main_element = true) ->
    try
      new_node = document.importNode node_template, true

      if is_main_element == true
        current_node?.remove()
        new_node.classList.add 'main-presentation-element'
        current_node = new_node

      else
        new_node.classList.add 'alt-presentation-element'
      presentation_box.appendChild new_node
      fs_button.style.display = "block"
      return new_node

    catch error
      unless node_template instanceof Node
        e = TypeError(
          'La variable node_template no es un Nodo HTML.')
        e.from = error
        throw e

      else
        throw error

updateFullScreenIcon = () ->
  if document.fullscreenElement or \
      document.mozFullScreenElement
    hideElements fs_button
    showElements ufs_button
  else
    hideElements ufs_button
    showElements fs_button

fullscreenClick = () ->
  if current_node?.requestFullscreen?
    presentation_box.requestFullscreen()

  else if current_node?.msRequestFullscreen?
    presentation_box.msRequestFullscreen()

  else if current_node?.mozRequestFullScreen?
    presentation_box.mozRequestFullScreen()

  else if current_node?.webkitRequestFullscreen?
    presentation_box.webkitRequestFullscreen()

unfullscreenClick = () ->
  # document.mozCancelFullscreen()
  if document.exitFullscreen?
    document.exitFullscreen()

  else if document.msExitFullscreen?
    document.msExitFullscreen()

  else if document.mozCancelFullScreen?
    document.mozCancelFullScreen()

  else if document.webkitExitFullscreen?
    document.webkitExitFullscreen()

#SETUP
fs_button.addEventListener 'click', fullscreenClick
#unless presentation_box.mozFullScreenEnabled
  #showElements(fs_button)
ufs_button.addEventListener 'click', unfullscreenClick
#if presentation_box.mozFullScreenEnabled
#  showElements(ufs_button)
full_screen_events = [
  'webkitfullscreenchange', 'mozfullscreenchange',
  'fullscreenchange', 'MSFullscreenChange']

for event in full_screen_events
  document.addEventListener event, updateFullScreenIcon




  document.addEventListener
