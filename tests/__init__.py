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

import openstack.common.config


def setup():
    log_file = tempfile.NamedTemporaryFile()
    openstack.common.config.set("logging", "logging_fd", sys.stdout)
    openstack.common.config.set("logging", "log_to_syslog", True)
    openstack.common.config.set("logging", "log_to_file", True)
    openstack.common.config.set("logging", "log_file", log_file.name)
