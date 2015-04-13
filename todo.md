-   add an in-place javascript insertion helper
-   solve this warning:
    
        export GEM_HOME=./gems && ./gems/bin/sass --update static/scss:static/css
          directory static/css
        WARNING: The box-sizing mixin is deprecated and will be removed in the next major version release. This property can now be used un-prefixed.
                 on line 410 of static/scss/bourbon_files/_bourbon-deprecated-upcoming.scss, in `box-sizing'
                 from line 5 of static/scss/base.scss

              write static/css/base.css
              write static/css/base.css.map
              write static/css/boxes.css
              write static/css/boxes.css.map
              write static/css/layout.css
              write static/css/layout.css.map

-   move this to the configuration:
    
        for module in app.ui_modules.values():
            if issubclass(module, BoilerUIModule):
                module.add_handler(app)
                
-   Replace chainmap in layout.html with just `globals()`.
     ~~evaluate if chainmap in layout.html can be replaced
     with dict.update~~
-   add code_related_message(print_f, code_path) in
    messages.py
-   add header-title id to the default titles
-   add proxy_url to conf package using a url method to
    concatenate all parts
