def add_ext_file(handler, filenames, static_url_func=None):
    if not hasattr(handler, 'ext_files'):
        handler.ext_files = []
        
    if not static_url_func:
        static_url_func = handler.static_url
    
    if isinstance(filenames, str):
        handler.ext_files.append(
            static_url_func(filenames)
        )
    else:
        handler.ext_files.extend(static_url_func(filename)
                                 for filename in filenames)
                                 
    return ''
