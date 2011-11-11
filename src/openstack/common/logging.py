from __future__ import absolute_import

import logging

import openstack.common.config as config


class Logger(logging.Logger):
    """Openstack logging entry point."""

    def __init__(self, name):
        """Initialize logger with a name."""
        self._name = name
        self._config = config.get_section("logging")

        log_file = self._config.get("log_file")
        syslog_device = self._config.get("syslog_device")
        publish_errors = self._config.get("publish_errors")

        stderr = logging.StreamHandler()
        self.addHandler(stderr)

        if syslog_device is not None:
            syslog = logging.SyslogHandler(syslog_device)
            self.addHandler(syslog)
            self.removeHandler(stderr)

        if log_file is not None:
            filelog = logging.WatchedFileHandler(log_file)
            self.addHandler(filelog)
            self.removeHandler(stderr)

        if publish_errors is True:
            publisher = PublishErrorsHandler()
            self.addHandler(publisher)
