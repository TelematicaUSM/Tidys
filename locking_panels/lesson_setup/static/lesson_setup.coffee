#VARIABLES

panel_id = 'lesson-setup-panel'
template = document.getElementById 'course-button-template'
spinner = document.getElementById 'lsp-spinner'
new_course_box = document.getElementById 'lsp-new-course'
select_course_box = document.getElementById(
    'lsp-select-course')
new_course_button = document.getElementById(
    'new-course-button')
cancel_button = document.getElementById 'lsp-cancel-button'
create_button = document.getElementById 'lsp-create-button'
new_course_name = document.getElementById 'new-course-name'

#FUNCTIONS

@showLessonSetup = ->
    switchToPanel(panel_id)

#SETUP
ws.getMessagePromise('tokenOk').then ->
    ws.sendSafeJSON
        'type': 'getCourses'

ws.getMessagePromise('courses').then (message) ->
    spinner.style.display = 'none'
    
    if message.courses.length is 0
        hideElements [new_course_button, select_course_box,
                      cancel_button]
        showElements new_course_box
    else
        hideElements new_course_box
        showElements [new_course_button, select_course_box]
        
    tbutton = template.content.querySelector 'button'
    for course in message.courses
        button = tbutton.cloneNode()
        button.textContent = course.name
        template.parentNode.appendChild button

new_course_button.addEventListener 'click', ->
    hideElements new_course_button
    showElements new_course_box

cancel_button.addEventListener 'click', ->
    hideElements new_course_box
    showElements new_course_button
    
ws.addMessageListener 'createCourseResult', (message) ->
    if message.result is 'ok'
        activatePanels()
    else if message.result is 'duplicate'
        showBubble('El curso que quiere crear ya existe!',
                   PRIMARY_COLOR)

create_button.addEventListener 'click', ->
    ws.sendSafeJSON
        'type': 'createCourse'
        'name': new_course_name.value
