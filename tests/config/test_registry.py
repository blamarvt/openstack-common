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
import tempfile

import unittest2 as unittest

import openstack.common.exceptions as exceptions
import openstack.common.config.registry as registry


class ConfigRegistryTestCase(unittest.TestCase):
    """Tests for configuration registry."""

    def test_get_nonexistant_option(self):
        """Try to get a configuration option that doesn't exist."""
        with self.assertRaises(exceptions.NoSuchConfigOption):
            registry.ConfigRegistry.get("section", None)

    def test_find_config_file(self):
        """Test the find_config_file functionality."""
        old_search_dirs = registry.ConfigRegistry.search_dirs
        temp_dir = tempfile.mkdtemp()

        temp_config = os.path.join(temp_dir, "openstack-common.conf")
        open(temp_config, 'a').close()

        registry.ConfigRegistry.search_dirs = [temp_dir]

        self.assertEquals(temp_config,
                          registry.ConfigRegistry.find_config_file())

        registry.ConfigRegistry.search_dirs = old_search_dirs
        os.remove(temp_config)
        os.removedirs(temp_dir)

    def test_load_from_path(self):
        """Tests loading a config from a file."""
        old_search_dirs = registry.ConfigRegistry.search_dirs
        temp_dir = tempfile.mkdtemp()

        temp_config = os.path.join(temp_dir, "openstack-common.conf")
        open(temp_config, 'a').close()
