import os
import sys
import time

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


class _TestResult(nose.result.TextTestResult):
    """Customized `nose.results.TextTestResult`."""

    _colorizers = [
        #_WindowsColorizer,
        #_ANSIColorizer,
    ]

    def __init__(self, *args, **kwargs):
        """Initialize test result."""
        show_elapsed = kwargs.pop("show_elapsed")
        nose.result.TextTestResult.__init__(self, *args, **kwargs)

        self._show_elapsed = show_elapsed
        self._num_slow_tests = 5
        self._slow_tests = []
        self._colorizer = None
        self._start_time = None

        for colorizer in self._colorizers:
            if colorizer.supported():
                self._colorizer = colorizer
                break

    def startTest(self, test):
        """Override default nose startTest logic."""
        self._start_time = time.time()
        if self.showAll:
            test_case_name = test.test.__class__.__name__
            self.stream.writeln(test_case_name)
            self.stream.writeln("")

class _TextTestRunner(nose.core.TextTestRunner):
    """Customized `nose.core:TextTestRunner`."""

    def __init__(self, *args, **kwargs):
        """Initialize our test runner."""
        self.show_elapsed = kwargs.pop("show_elapsed")
        nose.core.TextTestRunner(self, *args, **kwargs)

    def _makeResult(self):
        """Overrides original _makeResult."""
        return _TestResult(self.stream,
                           self.descriptions,
                           self.verbosity,
                           self.config,
                           show_elapsed=self.show_elapsed)

    def _writeSlowestTests(self, slow_tests):
        """Show the N slowests tests."""
        total_time = sum(test[0] for test in slow_tests)
        self.stream.writeln("Slowest %i tests took %.2f seconds:"
                                % (len(slow_tests), total_time))

        for elapsed_time, test in sorted(slow_tests, reverse=True):
            time_str = "%.2f" % elapsed_time
            self.stream.writeln("    %s %s" % (time_str.ljust(10), test))

    def run(self, test):
        """Overrides original 'run' method to display slow tests."""
        test_results = nose.core.TextTestRunner.run(self, test)
        if self.show_elapsed and test_results.slow_tests:
           self._writeSlowestTests(test_results.slow_tests)
        return test_results


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

        runner = TextTestRunner(stream=config.stream,
                                verbosity=config.verbosity,
                                config=config)

        return not nose.core.run(config=config,
                                 testRunner=runner,
                                 argv=argv)
