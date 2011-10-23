#!/usr/bin/env python

# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2010-2011 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Authentication-based WSGI middleware."""

import webob

try:
    import keystone.client
except ImportError:
    keystone = None

import openstack.common.wsgi.base
import openstack.common.wsgi.paste


class TokenAuth(openstack.common.wsgi.base.Middleware):
    """WSGI middleware for authenticating via HTTP header tokens."""

    def __init__(self, application, auth_url):
        """Initialize TokenAuth middleware.

        :param application: The WSGI application we're wrapping
        :param auth_url: The external authentication location

        """
        super(TokenAuth, self).__init__(application)
        self._auth_url = auth_url
        self._client = self._create_client(auth_url)

    @staticmethod
    def _create_client(auth_url):
        """Create and return a client to use for token validation."""
        if keystone is None:
            raise ImportError("keystone.client")
        return keystone.client.AdminClient(auth_url)

    def _reject_request(self):
        """Reject a request by raising an HTTP 401 exception.

        The WWW-Authenticate header is supplied with the URL where the
        client should authenticate.

        """
        body_msg = _("Authentication Required")
        header_msg = _("Authenticate at %s") % self._auth_url
        headers = [("WWW-Authenticate", header_msg)]
        raise webob.exc.HTTPUnauthorized(body_msg, headers)

    def _validate_token(self, token):
        """Validate the given token.

        :param token: String token of a non-specific length
        :returns: Response from the authentication service, or None if token
                  cannot be validated.

        """
        return self._client.validate_token(token)

    def _process_request(self, request):
        """Authenticate the given request.

        If the request contains a valid token, forward the request on to the
        rest of the WSGI stack. If the request does not contain a valid token,
        respond with HTTP 401.

        """
        # NOTE(blamar): Do we need to support X-Storage-Token too?
        token = request.headers.get("X-Auth-Token")

        if token is None:
            raise self._reject_request()

        auth_response = self._validate_token(token)

        if auth_response is None:
            raise self._reject_request()

        user = auth_response["access"]["user"]
        user_name = user["name"]
        tenant_id = 0  # NOTE(blamarvt): This does not seem to be returned
        roles = [role["name"] for role in user["roles"]]

        request.headers["X-Authorization"] = "Proxy %s" % user_name
        request.headers["X-Tenant-ID"] = tenant_id
        request.headers["X-User"] = user_name
        request.headers["X-Role"] = ",".join(roles)


class PasteTokenAuth(TokenAuth, openstack.common.wsgi.paste.Filter):
    pass
