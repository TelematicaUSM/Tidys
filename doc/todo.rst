General project tasks
=====================

.. todo::
    To do:
        -   Switch to ecmascript 6.
        -   Use
            ``msg.join_path(__name__, self.end.__qualname__)``
            instead of ``path``.
        -   Create a state transition table for the 5 user
            states and determine the actions that should be
            executed for every transition. Rewrite the login
            and logout functions according to the table.
        -   Close menu when a non manual panel change is
            executed.
        -   Include try and except statements in every
            coroutine to allow the exception to bubble to
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
        -   Describe the different panel classes.
        -   Send updates from the courses being dictated in
            each room to all students that are waiting to
            attend to a course.
        -   Add libjpeg-dev to dependencies in the makefile.
