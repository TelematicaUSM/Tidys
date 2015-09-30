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


def filter_classes(handler, iterable, classes):
    """Filter the objects of ``iterable`` by their classes.

    Return a list of objects, that is a subset of the
    objects in the ``iterable`` parameter and whose
    ``classes`` attribute coincide with at least one item in
    the ``classes`` argument.

    :param RequestHandler handler:
        The request handler that has called this
        ``ui_method``.

    :param Iterable iterable:
        Any iterable that contains objects with an attribute
        named ``classes``.

    :param set classes:
        A set of classes. Each class is a string.

    :return:
        A list of objects, that is a subset of the objects
        in the ``iterable`` parameter.

    :raises TypeError:
        If ``iterable`` is not an iterable or if ``classes``
        is not a set.

    :raises ValueError:
        If not all objects in iterable have the ``classes``
        attribute or if not all ``classes`` attributes of
        the objects in iterable are sets.
    """
    try:
        objects = list(iterable)

        return list(
            filter(lambda o: o.classes & classes, objects)
        )

    except AttributeError as ae:
        if not all(hasattr(o, 'classes') for o in objects):
            ve = ValueError(
                'Not all objects in iterable have the '
                'classes attribute.')
            raise ve from ae

        else:
            raise

    except TypeError as te:
        all_clss_are_sets = all(
            isinstance(o.classes, 'set') for o in objects)

        if not all_clss_are_sets:
            ve = ValueError(
                'Not all classes attributes of the '
                'objects in iterable are sets.')
            raise ve from te

        elif not isinstance(classes, set):
            e = TypeError(
                'The classes attribute has to be a set.')
            raise e from te

        else:
            raise
