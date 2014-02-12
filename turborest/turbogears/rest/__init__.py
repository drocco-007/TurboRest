import cherrypy

from turbogears.controllers import expose, Controller


def _default(self, *vpath, **kw):
    http_method = cherrypy.request.method
    method = getattr(self, http_method)

    # If there is a vpath, we tried to look up a sub-resource or other exposed
    # method and failed
    if vpath:
        raise cherrypy.HTTPError(404, 'Not found')
    elif not callable(method) or not getattr(method, 'exposed', False):
        raise cherrypy.HTTPError(405, '%s not allowed on %s' % (
            http_method, cherrypy.request.browser_url))

    return method(**kw)


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
    as its first parameter and a reference to the parent container as the
    second parameter.

    RESTContainers also do method-based dispatch if the decorated controller
    class does *not* define default::

    >>> @RESTContainer(CandidateResource)
    ... class CandidateRootController(Controller):
    ...    @expose()
    ...    def GET(self):
    ...        # handle request for /candidates

    """

    def decorator(controller_cls):
        def __getattr__(self, attribute):
            try:
                return resource_cls(int(attribute), self)
            except ValueError as e:
                return super(controller_cls, self).__getattr__(attribute)

        controller_cls.__getattr__ = __getattr__

        if not hasattr(controller_cls, 'default'):
            controller_cls.default = expose()(_default)

        return controller_cls

    return decorator


class RESTResource(Controller):
    """Controller base class that provides HTTP method-based dispatch.

    Subclasses should define methods for each HTTP method they wish to
    implement (e.g. ``GET``).

    See ``README.rst`` and ``controllers.py`` in the example application for
    example usages.

    """

    default = expose()(_default)
