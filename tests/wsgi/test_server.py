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

import time

import eventlet.patcher
import unittest2 as unittest

import openstack.common.test
import openstack.common.wsgi.server


class ServerTestCase(openstack.common.test.TestCase):
    """Tests for WSGI server."""

    def setUp(self):
        """Run before every test."""
        eventlet.monkey_patch()
        self.server = openstack.common.wsgi.server.Server(config=self.config,
                                                          name="test",
                                                          app=None)

    def test_wsgi_server_start_stop(self):
        self.server.start()
        time.sleep(0)  # FIXME: I sincerely hate sleeps
        self.assertEquals(self.server.host, "0.0.0.0")
        self.assertTrue(self.server.port > 0)
        self.server.stop()
        self.server.wait()
