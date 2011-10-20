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

import unittest2 as unittest
import webob.dec

import openstack.common.wsgi.base
import openstack.common.wsgi.middleware.auth


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

    def test_auth_with_invalid_auth_url(self):
        """Unable to connect to auth URL."""
        pass
