#VARIABLES

template = document.getElementById 'list-button-template'
tbutton = template.content.querySelector 'button'
spinner = document.getElementById 'ssp-spinner'
select_course_box = document.getElementById(
    'ssp-select-course')

#FUNCTIONS

@showStudentSetup = ->
    switchToPanel('student-setup-panel')

setCourse = (course_id) ->
    assign = ->
        ws.sendJSONIfOpen
            'type': 'studentSetup.course.set'
            'course_id': course_id

    ws.addMessageListener 'session.start.ok', assign
    assign()

#SETUP

ws.getMessagePromise('session.start.ok').then ->
    ws.sendSafeJSON
        'type': 'courses.room.get'

ws.getMessagePromise('studentSetup.course.set.ok').then ->
    activatePanels()

ws.getMessagePromise('courses').then (message) ->
    for course in message.courses
        button = document.importNode(tbutton, true)
        button.textContent =
            "#{ course.name } (#{ course.owner })"
        button.course_id = course._id
        button.addEventListener 'click', (event) ->
            setCourse(event.target.course_id)
        select_course_box.appendChild button

    hideElements spinner
    showElements select_course_box
