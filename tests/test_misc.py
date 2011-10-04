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


class ComplianceTestCase(unittest.TestCase):
    """Tests checking code/project compliance."""

    _jenkins_email = "<jenkins@review.openstack.org>"
    _top_dir = os.path.dirname(__file__) + '/..'

    def test_authors_up_to_date(self):
        """Ensure all committers are in AUTHORS file."""
        alias_map = {}
        alias_map[self._jenkins_email] = self._jenkins_email

        def _get_file(file_name):
            mailmap_path = os.path.join(self._top_dir, file_name)
            mailmap_file = open(mailmap_path, "r")
            with mailmap_file:
                yield mailmap_file.readline()

        for email in _get_file("AUTHORS"):
            email = "<%s>" % email.strip()
            alias_map[email] = email

        for mapping in _get_file(".mailmap"):
            primary, secondary = mapping.split(" ")
            alias_map[secondary.strip()] = primary.strip()

        command_string = ["git", "log", "--format=%ae"]
        command = subprocess.Popen(command_string, stdout=subprocess.PIPE)

        for git_author in command.communicate()[0].split():
            author = alias_map.get("<%s>" % git_author)
            if author is None:
                self.fail("Committer '%s' not in AUTHORS file." % git_author)
