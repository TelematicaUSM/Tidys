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

assignCourseToCurrentRoom = (course_id) ->
    assign = ->
        ws.sendJSONIfOpen
            'type': 'course.assignment.to_room'
            'course_id': course_id

    ws.addMessageListener 'session.start.ok', assign
    assign()

#SETUP

ws.getMessagePromise('session.start.ok').then ->
    ws.sendSafeJSON
        'type': 'getCourses'

ws.addMessageListener 'course.assignment.ok', activatePanels

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
        button = document.importNode(tbutton, true)
        button.textContent = course.name
        button.course_id = course._id
        button.addEventListener 'click', (event) ->
            assignCourseToCurrentRoom(
                event.target.course_id)
        template.parentNode.appendChild button

new_course_button.addEventListener 'click', ->
    hideElements new_course_button
    showElements new_course_box
    new_course_name.focus()

cancel_button.addEventListener 'click', ->
    hideElements new_course_box
    showElements new_course_button

create_button.addEventListener 'click', ->
    ws.sendSafeJSON
        'type': 'createCourse'
        'name': new_course_name.value

new_course_name.addEventListener 'input', ->
    if /\S/.test new_course_name.value
        create_button.disabled = false
    else
        create_button.disabled = true

new_course_name.addEventListener 'keyup', (e) ->
    if e.key is 'Enter' and not create_button.disabled
        create_button.click()

ws.addMessageListener 'createCourseResult', (message) ->
    switch message.result
        when 'ok' then assignCourseToCurrentRoom(
            message.course_id)

        when 'emptyName' then showErrorBubble(
            'El nombre pareciera estar vacío!')

        when 'duplicate' then showErrorBubble(
            'El curso que quiere crear ya existe!')

        else showErrorBubble(
            'No se ha podido crear el curso!')
