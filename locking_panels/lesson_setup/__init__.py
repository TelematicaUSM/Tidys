import src


class LessonSetupLockingPanel(
        src.boiler_ui_module.BoilerUIModule):
    _id = 'lesson-setup-panel'
    classes = {'scrolling-panel', 'system-panel'}
    conf = {
        'static_url_prefix': '/lesson_setup/',
        'static_path':
            './locking_panels/lesson_setup/static',
        'css_files': ['lesson_setup.css'],
        'js_files': ['lesson_setup.js'],
    }
    
    def render(self):
        return self.render_string(
            '../locking_panels/lesson_setup/'
            'lesson_setup.html', courses=[])
