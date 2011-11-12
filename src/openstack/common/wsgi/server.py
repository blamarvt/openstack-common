# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import eventlet.wsgi
import greenlet

import openstack.common.logging


class Server(object):
    """Eventlet-based WSGI server."""

    _default_pool_size = 1000
    _default_host = "0.0.0.0"
    _default_port = 0

    def __init__(self, name, app, host=None, port=None, pool_size=None):
        """Initialize eventlet-based WSGI server."""
        self.name = name
        self.host = host or self._default_host
        self.port = port or self._default_port
        self._app = app
        self._pool = eventlet.GreenPool(pool_size or self._default_pool_size)
        self._server = None
        self._socket = None
        self._logger = openstack.common.logging.Logger(self.name)

    def __start(self):
        """Start eventlet server."""
        eventlet.wsgi.server(self._socket,
                             self._app,
                             custom_pool=self._pool,
                             log=self._logger)

    def start(self, backlog=128):
        """Start eventlet thread which starts the server."""
        self._socket = eventlet.listen((self.host, self.port), backlog=backlog)
        self._server = eventlet.spawn(self.__start)
        (self.host, self.port) = self._socket.getsockname()

    def stop(self):
        """Stop the eventlet WSGI server."""
        self._server.kill()

    def wait(self):
        """Block, until the server has stopped.

        Waits on the server's eventlet to finish, then returns.

        :returns: None

        """
        try:
            self._server.wait()
        except greenlet.GreenletExit:
            pass
