def add_ext_file(handler, filename):
    if not hasattr(handler, 'ext_files'):
        handler.ext_files = []
    handler.ext_files.append(filename)
    return ''

def add_module_file(handler, filename):
    if not hasattr(handler, 'module_files'):
        handler.module_files = []
    handler.module_files.append(filename)
    return ''
