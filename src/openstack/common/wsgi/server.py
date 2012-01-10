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
import openstack.common.config.datatypes as config_types


class Server(object):
    """Eventlet-based WSGI server."""

    default_pool_size = 1000
    default_host = "0.0.0.0"
    default_port = 0

    def __init__(self, config, name, app):
        """Initialize eventlet-based WSGI server."""
        section = "%s_wsgi_server" % name

        config.define(section=section,
                      name="host",
                      datatype=config_types.String,
                      default=self.default_host,
                      description="The host IP to bind the server to.")

        config.define(section=section,
                      name="port",
                      datatype=config_types.Integer,
                      default=self.default_port,
                      description="The port to bind the server to.")

        config.define(section=section,
                      name="pool_size",
                      datatype=config_types.Integer,
                      default=self.default_pool_size,
                      description="The number of concurrent requests to "
                                  "allow for this server.")

        self._name = name
        self._app = app
        self._server = None
        self._socket = None
        self._logger = openstack.common.logging.Logger(config, name)

        self._host = config.get(section, "host")
        self._port = config.get(section, "port")
        self._pool = eventlet.GreenPool(config.get(section, "pool_size"))

    def __start(self):
        """Start eventlet server."""
        eventlet.wsgi.server(self._socket,
                             self._app,
                             custom_pool=self._pool,
                             log=self._logger)

    def start(self, backlog=128):
        """Start eventlet thread which starts the server."""
        addr = (self._host, self._port)
        self._socket = eventlet.listen(addr=addr, backlog=backlog)
        self._server = eventlet.spawn(self.__start)
        (self._host, self._port) = self._socket.getsockname()

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

    @property
    def host(self):
        """Read-only host property."""
        return self._host

    @property
    def port(self):
        """Read-only port property."""
        return self._port
