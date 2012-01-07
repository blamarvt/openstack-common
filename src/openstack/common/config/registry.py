import collections
import ConfigParser

import openstack.common.exceptions as exceptions


class Registry(object):
    """Used to store and retrieve config values."""

    def __init__(self):
        """Initialize a new configuration registry."""
        self._data = collections.defaultdict(dict)
        self._junk = collections.defaultdict(dict)
        self._parser = ConfigParser.ConfigParser()

    def get(self, section, option):
        """Return a particular option value."""
        try:
            # Returning a value in the config which has been 'defined'
            return self._data[section][option].from_parser(self._parser)
        except KeyError:
            # Requested value has not been 'defined'
            raise exceptions.NoSuchConfigOption(section=section, option=option)

    def set(self, section, option, value):
        """Set the value of a particular config option."""
        try:
            self._data[section][option].value = value
        except KeyError:
            # Value hasn't been defined yet, so throw it in junk
            self._junk[section][option] = value

    def load(self, config_file):
        """Load a configuration file into the registry."""
        self._parser.readfp(config_file)
        for section in self._parser.sections():
            for option, value in self._parser.items(section):
                self.set(section, option, value)

    def define(self, section, name, datatype, description, default=None):
        """Define a configuration option in the config registry.

        :param section: The config section this option belongs in
        :param name: The name of the config option
        :param datatype: The class/datatype of the config option
        :param description: A short description of the config option
        :param default: The default value for the config option
        :returns: None

        """
        item = datatype(name, description, default)
        if name in self._junk[section]:
            item.value = self._junk[section][name]

        self._data[section][name] = item
