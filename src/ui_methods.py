def add_ext_file(handler, filename):
    if not hasattr(handler, 'ext_files'):
        handler.ext_files = []
    handler.ext_files.append(filename)
    return ''
