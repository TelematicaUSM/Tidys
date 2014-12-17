from tornado.web import TemplateModule

class PanelLoader(TemplateModule):
    panels = {}
    
    @classmethod
    def register_panel(cls, panel_class):
        cls.panels[panel_class._id] = panel_class
        
    def render(self):
        def set_resources(**kwargs):
            if path not in self._resource_dict:
                self._resource_list.append(kwargs)
                self._resource_dict[path] = kwargs
            else:
                if self._resource_dict[path] != kwargs:
                    raise ValueError("set_resources called"
                                     "with different"
                                     "resources for the"
                                     "same template")
            return ""
        return self.render_string(path,
            set_resources=set_resources, **kwargs)
