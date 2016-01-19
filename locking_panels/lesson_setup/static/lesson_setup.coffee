# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#VARIABLES

template = document.getElementById 'list-button-template'
tbutton = template.content.querySelector 'button'

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
    switchToPanel('lesson-setup-panel')

assignCourseToCurrentRoom = (course_id) ->
    assign = ->
        ws.sendJSONIfOpen
            'type': 'course.assignment.to_room'
            'course_id': course_id

    ws.addMessageListener 'session.start.ok', assign
    assign()

#SETUP

ws.getMessagePromise('session.start.ok').then ->
    ws.sendJSON
        'type': 'courses.user.get'

ws.getMessagePromise('course.assignment.ok').then ->
    activatePanels()

ws.getMessagePromise('courses').then (message) ->
    for course in message.courses
        button = document.importNode(tbutton, true)
        button.textContent = course.name
        button.course_id = course._id
        button.addEventListener 'click', (event) ->
            assignCourseToCurrentRoom(
                event.target.course_id)
        select_course_box.appendChild button

    hideElements spinner

    if message.courses.length is 0
        hideElements [new_course_button, select_course_box,
                      cancel_button]
        showElements new_course_box
    else
        hideElements new_course_box
        showElements [new_course_button, select_course_box]

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
