"""Base class for other `openstack.common.wsgi` classes."""

import routes.middleware
import webob.dec


class Application(object):
    """WSGI application class."""

    @webob.dec.wsgify
    def __call__(self, request):
        """Called on every request to this application."""
        msg = _("WSGI applications must implemented __call__.")
        raise NotImplementedError(msg)


class Middleware(object):
    """WSGI middleware class."""

    def __init__(self, application):
        """Initialize middleware which will wrap the given application."""
        self.application = application

    def _process_request(self, _request):  # pylint: disable=R0201
        """Called on each request.

        If this returns None, the next application down the stack will be
        executed. If it returns a response then that response will be returned
        and execution will stop here.

        """
        return None

    def _process_response(self, response):  # pylint: disable=R0201
        """Do whatever you'd like to the response."""
        return response

    @webob.dec.wsgify
    def __call__(self, request):
        """Called on every request through this middleware."""
        response = self._process_request(request)

        if response is None:
            response = request.get_response(self.application)
            response = self._process_response(response)

        return response


class Router(object):
    """Routes WSGI requests using `routes` mapper."""

    def __init__(self, mapper):
        """
        Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        Examples:
          mapper = routes.Mapper()
          sc = ServerController()

          # Explicit mapping of one route to a controller+action
          mapper.connect(None, '/svrlist', controller=sc, action='list')

          # Actions are all implicitly defined
          mapper.resource('server', 'servers', controller=sc)

          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())

        """
        self.mapper = mapper
        self._router = routes.middleware.RoutesMiddleware(self.dispatch,
                                                          self.mapper)

    @webob.dec.wsgify
    def __call__(self, _request):
        """Route the incoming request to a controller."""
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def dispatch(request):
        """
        Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.
        """
        try:
            match = request.environ["wsgiorg.routing_args"][1]
        except KeyError:
            raise webob.exc.HTTPInternalServerError()

        if match is None:
            raise webob.exc.HTTPNotFound()

        return match["controller"]
