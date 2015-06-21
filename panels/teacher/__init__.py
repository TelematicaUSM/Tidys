import src


class TeacherPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'the-teacher-panel'
    classes = {'scrolling-panel', 'teacher-panel'}
    name = 'Teacher Panel'

    def render(self):
        return self.render_string(
            '../panels/teacher/teacher.html')
