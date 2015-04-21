import src


class StudentPanel(src.boiler_ui_module.BoilerUIModule):
    _id = 'the-student-panel'
    classes = {'scrolling-panel', 'student-panel'}
    name = 'Student Panel'
    
    def render(self):
        return self.render_string(
            '../panels/student/student.html')
