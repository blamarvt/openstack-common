from __future__ import absolute_import

import logging
import logging.handlers
import sys

import openstack.common.config as CONFIG


CONFIG.define(section="logging",
              name="log_to_fd",
              datatype=CONFIG.Boolean,
              default=True,
              description="If True, log to a file descriptor.")


CONFIG.define(section="logging",
              name="logging_fd",
              datatype=CONFIG.Object,
              default=sys.stderr,
              description="If log_to_fd, the file descriptor object to use.")


CONFIG.define(section="logging",
              name="log_to_syslog",
              datatype=CONFIG.Boolean,
              default=False,
              description="If True, syslog logging will be enabled.")


CONFIG.define(section="logging",
              name="log_to_file",
              datatype=CONFIG.Boolean,
              default=False,
              description="If True, file logging will be enabled.")


CONFIG.define(section="logging",
              name="syslog_device",
              datatype=CONFIG.String,
              default="/dev/log",
              description="The device to use for syslog logging. This "
                              "will only be used if log_to_syslog is True.")


CONFIG.define(section="logging",
              name="log_file",
              datatype=CONFIG.String,
              default="/var/log/$app_name.log",
              description="The log file to use if log_to_file is True.")


class Logger(logging.Logger):
    """Openstack logging entry point."""

    def __init__(self, name):
        """Initialize logger with a name."""
        logging.Logger.__init__(self, name)
        self._name = name

        for handler in self._get_handlers():
            self.addHandler(handler)

    def _get_handlers(self):
        """Read the config and determine which handlers will be used."""
        log_to_stderr = CONFIG.get("logging", "log_to_fd")
        if log_to_stderr is True:
            logging_fd = CONFIG.get("logging", "logging_fd")
            yield logging.StreamHandler(logging_fd)

        log_to_syslog = CONFIG.get("logging", "log_to_syslog")
        if log_to_syslog is True:
            syslog_device = CONFIG.get("logging", "syslog_device")
            yield logging.handlers.SysLogHandler(syslog_device)

        log_to_file = CONFIG.get("logging", "log_to_file")
        if log_to_file is True:
            log_file = CONFIG.get("logging", "log_file")
            yield logging.handlers.WatchedFileHandler(log_file)

    def write(self, message):
        """Write a message to the logger (INFO level)."""
        return self.info(message)
