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

import os
import subprocess
import sys

import unittest2 as unittest
import webob.dec
import webob.exc

import openstack.common.wsgi.base
import openstack.common.wsgi.paste as wsgi_paste
import openstack.common.wsgi.middleware.auth as auth_middleware


class PasteTestCase(unittest.TestCase):
    """Tests for `paste` deploy classes."""

    def test_app(self):
        global_conf = {}
        local_conf = {}
        result = wsgi_paste.Application.factory(global_conf, **local_conf)

    def test_filter(self):
        global_conf = {}
        local_conf = {}
        paste_filter = wsgi_paste.Filter.factory(global_conf, **local_conf)
        paste_filter(None)


class MiddlewareTestCase(unittest.TestCase):
    """Tests checking WSGI middleware."""

    def setUp(self):
        """Run before each test."""
        self.request = webob.Request.blank("/")

        @webob.dec.wsgify
        def app(request):
            return webob.Response("test_middleware")

        self.middleware = openstack.common.wsgi.base.Middleware(app)

    def test_middleware(self):
        expected = "test_middleware"
        actual = self.middleware(self.request).body

        self.assertEqual(expected, actual)

    def test_middleware_process_request(self):
        @webob.dec.wsgify
        def _process_request(request):
            return webob.Response("process_request")

        self.middleware._process_request = _process_request
        expected = "process_request"
        actual = self.middleware(self.request).body

        self.assertEqual(expected, actual)

    def test_middleware_process_response(self):
        @webob.dec.wsgify
        def _process_response(request):
            return webob.Response("process_response")

        self.middleware._process_response = _process_response
        expected = "process_response"
        actual = self.middleware(self.request).body

        self.assertEqual(expected, actual)


class ApplicationTestCase(unittest.TestCase):
    """Tests for base WSGI application class."""

    def test_wsgi_app_unimplemented(self):
        """Simple base WSGI app test."""
        request = webob.Request.blank("/")
        app = openstack.common.wsgi.base.Application()

        with self.assertRaises(NotImplementedError):
            app(request)


class AuthTestCase(unittest.TestCase):
    """Test cases for auth WSGI middleware."""

    _VALID_RESPONSE = {
        "access": {
            "user": {
                "name": "test_user",
                "roles": [{
                    "name": "role1",
                },
                {
                    "name": "role2",
                }],
            },
        },
    }

    def _create_client(self, auth_url):
        return self.admin_client

    def _validate_token(self, token):
        return self.token_response

    @webob.dec.wsgify
    def _test_app(self, request):
        return webob.Response("test_auth")

    def setUp(self):
        """Run before each test."""
        self.request = webob.Request.blank("/")
        self.app = self._test_app

        # Simple AdminClient for tests
        class AdminClient(object):
            def __init__(self, test_class):
                self._tc = test_class

            @property
            def auth_url(self):
                return self._tc.auth_url

            def validate_token(self, token):
                return self._tc.token_response

        self.client = AdminClient(self)
        self.token_response = None
        self.auth_url = "http://example.com"
        self.middleware = auth_middleware.TokenAuth(self.app, self.client)

    def test_auth_with_no_token(self):
        """Unable to validate token because it is not passed."""
        with self.assertRaises(webob.exc.HTTPUnauthorized):
            self.middleware(self.request)

    def test_auth_with_invalid_token(self):
        """Unable to validate token, validate_token returns None."""
        self.request.headers["X-Auth-Token"] = "invalid_token"
        with self.assertRaises(webob.exc.HTTPUnauthorized):
            self.middleware(self.request)

    def test_auth_with_valid_token(self):
        """Able to validate token, validate_token returns object."""
        self.request.headers["X-Auth-Token"] = "valid_token"
        self.token_response = self._VALID_RESPONSE
        self.middleware(self.request)

    def test_auth_with_valid_token_bad_response(self):
        """Able to validate token, but get back bad response."""
        self.request.headers["X-Auth-Token"] = "valid_token_bad_response"
        self.token_response = {}
        with self.assertRaises(webob.exc.HTTPUnauthorized):
            self.middleware(self.request)

    def test_auth_with_valid_token_bad_response_type(self):
        """Able to validate token, but get back bad response."""
        self.request.headers["X-Auth-Token"] = "valid_token_bad_response"
        self.token_response = ""
        with self.assertRaises(webob.exc.HTTPUnauthorized):
            self.middleware(self.request)
