def add_ext_file(handler, filename):
    if not hasattr(handler, 'ext_files'):
        handler.ext_files = []
    handler.ext_files.append(filename)
    return ''

def filter_classes(handler, iterable, classes):
    return list(
        filter(lambda i: i.classes & classes, iterable)
    )