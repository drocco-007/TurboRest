TurboRest
=========

TurboRest provides an alternative to the cumbersome RESTMethod bundled with
TurboGears 1.5. It supplies two abstractions


``RESTResource``
    Controller base class that provides HTTP method-based dispatch:

    .. code-block:: python

        class CandidateResource(RESTResource):
            def __init__(self, id):
                super(CandidateResource, self).__init__()
                self.candidate_id = id

            @expose()
            def GET(self):
                return {'success': True, 'candidate': {'id': self.candidate_id}}

            @expose()
            def POST(self):
                """Do POST-y things"""


``RESTContainer``
    Class decorator for creating containers of a specified resource. For
    example, to create a list of candidate resources such that::

        /candidates/<id>

    returns a candidate resource for the specified candidate, define the
    candidates controller as

    .. code-block:: python

        @RESTContainer(CandidateResource)
        class CandidateRootController(Controller):
            pass


    The resource class must have a constructor that takes a single integer ID
    as its parameter.

The `controllers.py`_  in the example application provides a more complete
demonstration of how the two abstractions fit together.

.. _controllers.py: https://github.com/drocco-007/TurboRest/blob/master/turborest_example/controllers.py


TurboRest Plugin
----------------

TurboRest is defined as a TurboGears plugin that will be automatically included
by TurboGears once the TurboRest package is installed. To use it, simply
import from the ``turbogears.rest`` namespace:

.. code-block:: python

    from turbogears.rest import RESTResource, RESTContainer


TurboRest Example
-----------------

TurboRest includes an example application demonstrating a basic structure. It
can be invoked with::

    python start-rest-example.py

