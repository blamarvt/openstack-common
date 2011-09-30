import os
import sys

import nose.core


class TestRunner(object):

    def __init__(self, strategy=None):
        """Initialize a test runner.

        :param strategy: Class used to determine how tests are run
        :returns: None

        """
        self._strategy = strategy or NoseTestRunStrategy()

    def run(self, test_directory, argv=None):
        """Run tests, outputting results to sys.stdout.

        :param argv: The input arguments, normally sys.argv
        :returns: A valid return code, normally passed to sys.exit

        """
        return self._strategy.run(test_directory, argv)


class NoseTestRunStrategy(object):

    def run(self, test_directory, argv=None):
        """Initialize a nose-specific test running strategy.

        :param test_directory: A directory containing tests to run.
        :param argv: The input arguments, defaults to sys.arg
        :returns: A valid return code, normally passed to sys.exit

        """
        argv = argv or sys.argv

        config = nose.config.Config(stream=sys.stdout,
                                    env=os.environ,
                                    verbosity=2,
                                    workingDir=test_directory,
                                    plugins=nose.core.DefaultPluginManager())

        runner = nose.core.TextTestRunner(stream=config.stream,
                                          verbosity=config.verbosity,
                                          config=config)

        return not nose.core.run(config=config,
                                 testRunner=runner,
                                 argv=argv)


