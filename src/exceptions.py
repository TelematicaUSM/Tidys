class NotDictError(TypeError):
    """Raise when an object is not an instance of dict.

    .. automethod:: __init__
    """

    def __init__(self, name, *args):
        """Initialize a new NotDictError.

        :param str name:
            Name of the object that is not a dictionary.
        """
        super().__init__(
            '{} is not a dictionary.'.format(name),
            *args
        )
