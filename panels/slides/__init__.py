# -*- coding: UTF-8 -*-

import json
from base64 import b64decode

from tornado.gen import coroutine

import src
from src.db import DBObject, db
from src.exceptions import NotDictError, NotStringError, \
    MissingFieldError
from src.utils import standard_name
from src.wsclass import subscribe


class SlidesPanel(src.boiler_ui_module.BoilerUIModule):
    id_ = 'slides-panel'
    classes = {'scrolling-panel', 'teacher-panel'}
    name = 'Diapositivas'
    conf = {
        'static_url_prefix': '/slides/',
        'static_path': './panels/slides/static',
        'css_files': ['slides.css'],
        'js_files': ['slides.js'],
    }

    def render(self):
        return self.render_string(
            '../panels/slides/slides.html')


class Slide(DBObject):
    coll = db.slides

    @classmethod  # noqa
    @coroutine
    def create(cls, user, data):
        """Create a new slideshow document in the database.

        :param src.bd.User user:
            The user that will own the slideshow.

        :param dict data:
            The data that should be used to create the new
            slideshow object.

            ``data`` should have the following format:

            .. code-block:: python

                {
                    'name': 'Slideshow Name',
                    'slides': [
                        {
                            'url': 'my.slides.com#slide1',
                            'question': {
                                'type': 'alternatives',
                                'wording': 'A question?',
                                'answers': [
                                    'Answer 1.',
                                    'Answer 2.',
                                    ...
                                ]
                            }
                        },
                        ...
                    ]
                }

            Where ``'Slideshow Name'`` should be the name of
            the slideshow, ``'my.slides.com#slide1'`` can be
            any valid URL, ``'A question?'`` should be an
            associated question to be asked using this slide
            and ``'Answer #.'`` are the different answer
            alternatives for the question.

            Currently the only supported question type is
            ``'alternatives'``.

            A presentation can have any number of slides and
            a question can have any number of answers.

            The object associated to the key ``'question'``
            can be ``None`` (``'question': None``).

        :return:
            A new slideshow object.
        :rtype: :class:`Slide`

        :raises AttributeError:
            If ``user`` has no attribute ``id``.

        :raises NotDictError:
            If ``data`` is not a dictionary.

        :raises NotStringError:
            If ``user.id`` or ``data['name']`` is not a
            string.

        :raises KeyError:
            If ``data`` has no key ``name``.

        :raises pymongo.errors.OperationFailure:
            If an database error occurred during creation.

        :raises pymongo.errors.DuplicateKeyError:
            If an object with the same id alredy exists in
            the database.
            :class:`~pymongo.errors.DuplicateKeyError` is a
            subclass of
            :class:`~pymongo.errors.OperationFailure`.

        :raises ConditionNotMetError:
            If the just created slide document no longer
            exists in the database. This should never
            happen!
        """
        try:
            id_ = user.id + standard_name(data['name'])
            self = yield super().create(id_)
            data['user_id'] = user.id
            yield self.store_dict(data)
            return self

        except AttributeError as e:
            if not hasattr(user, 'id'):
                ae = AttributeError(
                    "'user' has no attribute 'id'")
                raise ae from e

            else:
                raise

        except TypeError as te:
            if not isinstance(data, dict):
                raise NotDictError('data') from te

            elif not isinstance(data['name'], str):
                raise NotStringError("data['name']") from te

            elif not isinstance(user.id, str):
                raise NotStringError('user.id') from te

            else:
                raise

        except KeyError as e:
            if 'name' not in data:
                ke = KeyError("'data' has no key 'name'")
                raise ke from e

            else:
                raise

        except:
            raise

    @classmethod
    @coroutine
    def get_user_slide_list(cls, user):
        try:
            yield db.users.ensure_index('user_id')
            slides = yield cls.get_list(
                {'user_id': user.id},
                ['_id', 'name']
            )
            return slides

        except:
            raise  ###################################


class SlidesWSC(src.wsclass.WSClass):
    class parses(object):
        parser_names = {}

        def __init__(self, mime_type):
            self.mime_type = mime_type

        def __call__(self, meth):
            self.parser_names[self.mime_type] = \
                meth.__name__
            return meth

    def __init__(self, handler):
        super().__init__(handler)

        self.parsers = {
            mime_type: getattr(self, meth_name)
            for mime_type, meth_name in
            self.parses.parser_names.items()
        }

    @subscribe('slides.list.get')
    @coroutine
    def send_slide_list(self, message=None):
        try:
            slides = yield Slide.get_user_slide_list(
                self.handler.user)

        except:
            raise  ########################

        else:
            self.pub_subs['w'].send_message(
                {'type': 'slides', 'slides': slides})

    @subscribe('slides.add')
    @coroutine
    def add_slides(self, message):
        try:
            mime_type = message['mime']
            data = self.parsers[mime_type](message['data'])
            slide = yield Slide.create(
                self.handler.user, data)

        except Exception as e:
            raise
            self.pub_subs['w'].send_message(
                {
                    'type': 'slides.add.error',
                    'cause': str(e),
                    'message':
                        'Ocurrió una excepción dutante la '
                        'creación de la nueva presentación.'
                }
            )
            ##############################

        else:
            self.pub_subs['w'].send_message(
                {
                    'type': 'slides.add.ok',
                    'id': slide.id,
                    'name': slide.name,
                }
            )

    @parses('application/json')
    def json_parser(self, data):
        try:
            bytes_ = b64decode(data)
            json_ = bytes_.decode()
            data = json.loads(json_)

            if 'name' not in data:
                raise MissingFieldError('data', 'name')

            elif 'slides' not in data:
                raise MissingFieldError('data', 'slides')

            elif not isinstance(data['name'], str):
                raise NotStringError("data['name']")

            elif not isinstance(data['slides'], list):
                raise TypeError(
                    "data['slides'] should be a list.")

            elif len(data['slides']) < 1:
                raise ValueError(
                    "data['slides'] should have at least "
                    "one slide.")

            elif not all(
                    'url' in s for s in data['slides']):
                raise MissingFieldError('All slides', 'url')

            else:
                return data

        except:
            raise
