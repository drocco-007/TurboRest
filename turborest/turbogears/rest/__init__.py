import cherrypy

from turbogears.controllers import expose, Controller


def RESTContainer(resource_cls):
    """Class decorator for implementing REST-style container controllers.

    For example, to create a list of candidate resources such that::

        /candidates/<id>

    returns a candidate resource for the specified candidate, define the
    candidates controller as

    >>> class CandidateResource(RESTResource):
    ...     "Represents a single candidate"

    >>> @RESTContainer(CandidateResource)
    ... class CandidateRootController(Controller):
    ...    pass

    The resource class must have a constructor that takes a single integer ID
    as its parameter.

    """

    def decorator(controller_cls):
        def __getattr__(self, attribute):
            try:
                return resource_cls(int(attribute), self)
            except ValueError as e:
                return super(controller_cls, self).__getattr__(attribute)

        controller_cls.__getattr__ = __getattr__

        return controller_cls

    return decorator


class RESTResource(Controller):
    """Controller base class that provides HTTP method-based dispatch.

    Subclasses should define methods for each HTTP method they wish to
    implement (e.g. ``GET``).

    See ``README.rst`` and ``controllers.py`` in the example application for
    example usages.

    """

    @expose()
    def default(self, *vpath, **kw):
        http_method = cherrypy.request.method
        method = getattr(self, http_method)

        if not callable(method) or not getattr(method, 'exposed', False):
            raise cherrypy.HTTPError(405, '%s not allowed on %s' % (
                http_method, cherrypy.request.browser_url))
        return method(*vpath, **kw)
