import collections
import ConfigParser

import openstack.common.exceptions as exceptions


class Registry(object):
    """Used to store and retrieve config values."""

    def __init__(self):
        """Initialize a new configuration registry."""
        self._data = collections.defaultdict(dict)
        self._parser = ConfigParser.ConfigParser()

    def get(self, section, option):
        """Return a particular option value."""
        try:
            return self._data[section][option].from_parser(self._parser)
        except KeyError:
            raise exceptions.NoSuchConfigOption(section=section, option=option)

    def load(self, config_file):
        """Load a configuration file into the registry."""
        self._parser.readfp(config_file)

    def define(self, section, name, datatype, description, default=None):
        """Define a configuration option in the config registry.

        :param section: The config section this option belongs in
        :param name: The name of the config option
        :param datatype: The class/datatype of the config option
        :param description: A short description of the config option
        :param default: The default value for the config option
        :returns: None

        """
        self._data[section][name] = datatype(name, description, default)
