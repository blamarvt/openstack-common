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
import StringIO

import unittest2 as unittest

import openstack.common.config as config
import openstack.common.config.registry
import openstack.common.exceptions as exceptions


class ConfigRegistryTestCase(unittest.TestCase):
    """Tests for configuration registry."""

    test_config = """
        [logging]
        blah=test
        log_file=override
    """.strip().replace("\n        ", "\n")

    def test_get_nonexistant_option(self):
        """Try to get a configuration option that doesn't exist."""
        registry = openstack.common.config.registry.Registry()
        with self.assertRaises(exceptions.NoSuchConfigOption):
            registry.get("section", None)

    def test_find_config_file(self):
        """Test the find_config_file functionality."""
        os_path_exists = os.path.exists
        try:
            os.path.exists = lambda path: path == "/etc/test_app.conf"
            self.assertEquals("/etc/test_app.conf",
                              config.find_config("test_app"))
        finally:
            os.path.exists = os_path_exists

    def test_load_registry_undefined(self):
        """Test loading the registry."""
        registry = openstack.common.config.registry.Registry()
        registry.load(StringIO.StringIO(self.test_config))
        with self.assertRaises(exceptions.NoSuchConfigOption):
            registry.get("logging", "blah")

    def test_load_registry_then_define(self):
        """Test loading the registry."""
        registry = openstack.common.config.registry.Registry()
        registry.load(StringIO.StringIO(self.test_config))
        registry.define(section="logging",
                        name="log_file",
                        datatype=config.String,
                        default="default",
                        description="Test description.")
        self.assertEquals("override", registry.get("logging", "log_file"))

    def test_define_then_load_registry(self):
        """Test loading the registry."""
        registry = openstack.common.config.registry.Registry()
        registry.define(section="logging",
                        name="log_file",
                        datatype=config.String,
                        default="default",
                        description="Test description.")
        registry.load(StringIO.StringIO(self.test_config))
        self.assertEquals("override", registry.get("logging", "log_file"))




#        old_search_dirs = registry.ConfigRegistry.search_dirs
#        temp_dir = tempfile.mkdtemp()
#
#        temp_config = os.path.join(temp_dir, "openstack-common.conf")
#        open(temp_config, 'a').close()
#
#        registry.ConfigRegistry.search_dirs = [temp_dir]
#
#        self.assertEquals(temp_config,
#                          registry.ConfigRegistry.find_config_file())
#
#        registry.ConfigRegistry.search_dirs = old_search_dirs
#        os.remove(temp_config)
#        os.removedirs(temp_dir)
#
#    def test_load_from_path(self):
#        """Tests loading a config from a file."""
#        old_search_dirs = registry.ConfigRegistry.search_dirs
#        temp_dir = tempfile.mkdtemp()
#
#        temp_config = os.path.join(temp_dir, "openstack-common.conf")
#        open(temp_config, 'a').close()
