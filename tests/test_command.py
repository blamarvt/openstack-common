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

import openstack.common.command
import openstack.common.test


class CommandRegistryTestCase(openstack.common.test.TestCase):
    """Tests for command registry."""

    def setUp(self):
        self._registry = openstack.common.command.Registry(self.config)

    def test_add_retrieve_command(self):
        class MyCommand(object):
            name = "MyCommand"
        self._registry.add(MyCommand, version=100)
        expected = MyCommand
        actual = self._registry.get("MyCommand", version=100)
        self.assertEquals(expected, actual)
