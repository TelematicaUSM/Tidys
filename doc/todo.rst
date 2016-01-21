General project tasks
=====================

.. todo::
    To do:
        -   Modulo de alternativas. (pip)
        -   Create a room message type. (craguila)
        -   Parser HTML. (cganterh)
        -   Creación de grupos (juntar a dos personas).
        -   Boton para ir a la diapo n.
        -   Boton para cambiar de diapo desde las diapos.
        -   En home crear un box de login aparte de la
            descripción.
        -   Agregar botones para eliminar cursos y
            presentaciones.
        -   Parser PDF.
        -   Send updates from the courses being dictated in
            each room to all students that are waiting to
            attend to a course.
        -   Use
            ``msg.join_path(__name__, self.end.__qualname__)``
            instead of ``path``.
        -   Include try and except statements in every
            coroutine to allow the exceptions to bubble to
            the top and avoid being trapped by the
            coroutine.
        -   Wrap all code that is supposed to run at module
            import in a start function. So that linter
            doesn't complain about imported modules that are
            never used.
        -   lesson_setup.coffee allows the client to
            register the current course after regaining
            connection. But this works only in the client
            that originally registered the course. This
            should be done by all clients.
        -   qrmaster's main html output should be named
            index.html.
        -   This is not a good idea::

                ws.sendJSON(
                    {
                        'type': 'toDatabase',
                        'content': {
                            'type': 'courseMessage(117984339433749478236hola!!)',
                            'content': {
                                'type': 'logout',
                                'reason': 'hack'
                            }
                        }
                    }
                )
