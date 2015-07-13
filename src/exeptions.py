class NotDictError(TypeError):

    """Raise when an object is not an instance of dict."""

    def __init__(self, name, *args):
        super().__init__(
            '{} is not a dictionary.'.format(name),
            *args
        )
