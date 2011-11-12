from __future__ import absolute_import

import logging
import logging.handlers

import openstack.common.config as CONFIG


CONFIG.add_option(section="logging",
                  name="log_to_stderr",
                  datatype=CONFIG.Boolean,
                  default=True,
                  description="If True, stderr logging will be enabled.")


CONFIG.add_option(section="logging",
                  name="log_to_syslog",
                  datatype=CONFIG.Boolean,
                  default=False,
                  description="If True, syslog logging will be enabled.")


CONFIG.add_option(section="logging",
                  name="log_to_file",
                  datatype=CONFIG.Boolean,
                  default=False,
                  description="If True, file logging will be enabled.")


CONFIG.add_option(section="logging",
                  name="syslog_device",
                  datatype=CONFIG.String,
                  default="/dev/log",
                  description="The device to use for syslog logging. This "
                              "will only be used if log_to_syslog is True.")


CONFIG.add_option(section="logging",
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
        self._config = CONFIG.get_section("logging")

        for handler in self._get_handlers():
            self.addHandler(handler)

    def _get_handlers(self):
        """Read the config and determine which handlers will be used."""
        log_to_stderr = self._config.get("log_to_stderr")
        if log_to_stderr is True:
            yield logging.StreamHandler()

        log_to_syslog = self._config.get("log_to_syslog")
        if log_to_syslog is True:
            syslog_device = self._config.get("syslog_device")
            yield logging.handlers.SysLogHandler(syslog_device)

        log_to_file = self._config.get("log_to_file")
        if log_to_file is True:
            log_file = self._config.get("log_file")
            yield logging.handlers.WatchedFileHandler(log_file)

    def write(self, message):
        """Write a message to the logger (INFO level)."""
        return self.info(message)
