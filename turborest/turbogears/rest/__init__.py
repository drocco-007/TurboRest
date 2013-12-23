import cherrypy

from turbogears.controllers import expose, Controller


def RESTContainer(resource_cls):
    def decorator(controller_cls):
        def __getattr__(self, attribute):
            try:
                return resource_cls(int(attribute))
            except ValueError:
                super(controller_cls, self).__getattr__(attribute)

        controller_cls.__getattr__ = __getattr__

        return controller_cls

    return decorator


class RESTResource(Controller):
    @expose()
    def default(self, *vpath, **kw):
        http_method = cherrypy.request.method
        method = getattr(self, http_method)

        if not callable(method) or not getattr(method, 'exposed', False):
            raise cherrypy.HTTPError(405, '%s not allowed on %s' % (
                http_method, cherrypy.request.browser_url))

        return method(*vpath, **kw)
