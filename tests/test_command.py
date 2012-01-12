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
import openstack.common.exceptions as exceptions
import openstack.common.test


class CommandRegistryTestCase(openstack.common.test.TestCase):
    """Tests for command registry."""

    def setUp(self):
        self._registry = openstack.common.command.Registry()

    def test_add_retrieve_command(self):
        self._registry.add(openstack.common.command.Command)
        expected = openstack.common.command.Command
        actual = self._registry.get("Command", version=1)
        self.assertEquals(expected, actual)

    def test_retrieve_nonexistant_command(self):
        with self.assertRaises(exceptions.NoSuchCommand):
            self._registry.get("Command", version=1)


class CommandTestCase(openstack.common.test.TestCase):
    """Tests for commands."""

    def test_execute_command(self):
        cmd = openstack.common.command.Command()
        self.assertEquals(None, cmd())


class RemoteCommandTestCase(openstack.common.test.TestCase):
    """Tests for remote command handling."""

    def test_send_recv_remote_command(self):
        remote_cmd = openstack.common.command.RemoteCommand(self.config)
        cmd = openstack.common.command.EchoCommand(1, a=2)
        remote_cmd.send(cmd, "test_service", "test_host")
        expected = ((1,), {"a":2})
        actual = remote_cmd.recv("test_service", "test_host")()
        self.assertEquals(expected, actual)
