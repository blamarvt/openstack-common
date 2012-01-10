from __future__ import absolute_import

import logging
import logging.handlers
import sys

import openstack.common.config.datatypes as config_types


class Logger(logging.Logger):
    """Openstack logging entry point."""

    default_log_to_fd = True
    default_logging_fd = sys.stderr
    default_log_to_syslog = False
    default_log_to_file = False
    default_syslog_device = "/dev/log"
    default_log_file = "/var/log/openstack.log"

    def __init__(self, config, name):
        """Initialize logger with a name."""
        logging.Logger.__init__(self, name)
        self._name = name

        config.define(section="logging",
                      name="log_to_fd",
                      datatype=config_types.Boolean,
                      default=self.default_log_to_fd,
                      description="If True, log to a file descriptor.")

        config.define(section="logging",
                      name="logging_fd",
                      datatype=config_types.Object,
                      default=self.default_logging_fd,
                      description="If log_to_fd, the file descriptor object "
                                  "to use.")

        config.define(section="logging",
                      name="log_to_syslog",
                      datatype=config_types.Boolean,
                      default=self.default_log_to_syslog,
                      description="If True, syslog logging will be enabled.")

        config.define(section="logging",
                      name="log_to_file",
                      datatype=config_types.Boolean,
                      default=self.default_log_to_file,
                      description="If True, file logging will be enabled.")

        config.define(section="logging",
                      name="syslog_device",
                      datatype=config_types.String,
                      default=self.default_syslog_device,
                      description="The device to use for syslog logging. "
                                  "This will only be used if log_to_syslog "
                                  "is True.")

        config.define(section="logging",
                      name="log_file",
                      datatype=config_types.String,
                      default=self.default_log_file,
                      description="The log file to use if log_to_file "
                                  "is True.")

        log_to_stderr = config.get("logging", "log_to_fd")
        if log_to_stderr is True:
            logging_fd = config.get("logging", "logging_fd")
            self.addHandler(logging.StreamHandler(logging_fd))

        log_to_syslog = config.get("logging", "log_to_syslog")
        if log_to_syslog is True:
            syslog_device = config.get("logging", "syslog_device")
            self.addHandler(logging.handlers.SysLogHandler(syslog_device))

        log_to_file = config.get("logging", "log_to_file")
        if log_to_file is True:
            log_file = config.get("logging", "log_file")
            self.addHandler(logging.handlers.WatchedFileHandler(log_file))

    def write(self, message):
        """Write a message to the logger (INFO level)."""
        return self.info(message)
