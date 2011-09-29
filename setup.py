#!/usr/bin/env python

# Copyright 2010 OpenStack, LLC
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

import distutils.core
import subprocess

import setuptools


class CodeComplianceCommand(distutils.core.Command):

    description = "check for various code compliance violations"
    user_options = [
        ("pep8", None, "Perform pep8 checks"),
        ("pylint", None, "Perform pylint checks"),
    ]

    def initialize_options(self):
        self.pep8 = False
        self.pylint = False

    def finalize_options(self):
        pass

    def output_process(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output = process.communicate()[0]
        if output:
            print output

    def run(self):
        if self.pep8:
            print "Running PEP8 checks..."
            self.output_process("./tools/pep8")

        if self.pylint:
            print "Running pylint checks..."
            self.output_process("./tools/pylint")


setuptools.setup(
    name="openstack-common",
    version="1.1.1",
    description="Library for components common to multiple OpenStack projects.",
    author="OpenStack, LLC",
    author_email="openstack@lists.launchpad.net",
    url="http://www.openstack.org/",
    setup_requires=["nose"],
    test_suite = "nose.collector",
    packages=setuptools.find_packages(where="src"),
    package_dir={"openstack": "src/openstack"},
    cmdclass={"code_compliance": CodeComplianceCommand},
)
