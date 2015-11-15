# -*- coding: UTF-8 -*-

from .wsclass import CoursesWSC  # noqa
from . import patches            # noqa


class CourseIsNotDefined(AttributeError):
    """Raise when ``course`` is not defined.

    ``course`` should be defined in the current instance of
    :class:`~controller.MSGHandler`.

    .. automethod:: __init__
    """

    def __init__(self, *args):
        """Initialize a new CourseIsNotDefined exception."""
        super().__init__(
            'Attempted to use the `course` attribute, but '
            'the attribute is not assigned.',
            *args
        )
