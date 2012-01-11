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

import sys
import tempfile

import unittest2 as unittest

import openstack.common.config


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Initialize this test case."""
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.config = openstack.common.config.Registry()
        self.config.set("logging", "logging_fd", sys.stdout)
        self.config.set("logging", "log_to_syslog", True)
        self.config.set("logging", "log_to_file", True)

        log_file = tempfile.NamedTemporaryFile()
        self.config.set("logging", "log_file", log_file.name)
