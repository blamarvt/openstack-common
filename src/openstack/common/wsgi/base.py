"""Base class for other `openstack.common.wsgi` classes."""

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
