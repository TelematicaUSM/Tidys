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
        button = document.importNode tbutton, true
        button.textContent =
            "#{ course.name } (#{ course.owner })"
        button.course_id = course._id
        button.addEventListener 'click', (event) ->
            setCourse(event.target.course_id)
        select_course_box.appendChild button

    hideElements spinner
    showElements select_course_box
