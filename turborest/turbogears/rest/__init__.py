import inspect

import cherrypy
from turbogears.controllers import expose, Controller


import logging
log = logging.getLogger('turbogears.rest')


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


def RESTContainer(resource_cls_or_name=None):
    """Class decorator for implementing REST-style container controllers.

    For example, to create a list of candidate resources such that::

        /candidates/<id>

    returns a candidate resource for the specified candidate, define the
    candidates controller as

    >>> @RESTContainer('CandidateResource')
    ... class CandidateRootController(Controller):
    ...    pass

    >>> class CandidateResource(RESTResource):
    ...     "Represents a single candidate"

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

    For most resource containers, it is assumed that the resource class uses
    integer identifiers, and the int() function is used to determine that a
    resource is being requested: non-integer attribute requests are assumed to
    be requests for attributes on the container itself.

    If the resource class defines a valid_id static function, it is used in
    preference to the int function to determine if an attribute request should
    return an instance of the container's resource class. The valid_id function
    should take a single argument and return it if it is a valid identifier or
    raise ValueError if it is not.

    """

    def decorator(controller_cls):
        def resolve_resource(obj):
            try:
                _cls = obj.resource_cls
            except AttributeError:
                try:
                    module = inspect.getmodule(type(obj))
                    _cls = obj.resource_cls = getattr(module,
                                                      resource_cls_or_name)
                except (TypeError, AttributeError):
                    _cls = obj.resource_cls = resource_cls_or_name

            return _cls

        def _cp_dispatch(self, vpath):
            log.debug('%s vpath: %s', type(self).__name__, vpath)

            try:
                resource_id = vpath[0]
                resource_cls = resolve_resource(self)
                id_validator = getattr(resource_cls, 'valid_id', str)
                return resource_cls(id_validator(resource_id), self)
            except ValueError as e:
                log.debug('Invalid resource id: %s (%s: %s)',
                          resource_id,
                          type(e).__name__,
                          e)
                return vpath

        controller_cls._cp_dispatch = _cp_dispatch

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
