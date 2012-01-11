import collections

import openstack.common.config.datatypes as config_types


class Registry(object):
    """Command registry."""

    default_version = 1

    def __init__(self, config):
        """Initialize a new registry."""
        section = "command_registry"

        config.define(section=section,
                      name="default_version",
                      datatype=config_types.Integer,
                      default=self.default_version,
                      description="Default version of commands to use.")

        self._commands = collections.defaultdict(dict)
        self._default_version = config.get(section, "default_version")

    def add(self, command_cls, version=None):
        """Register a new command with the registry."""
        version = version or self._default_version
        self._commands[version][command_cls.name] = command_cls

    def get(self, command_name, version=None):
        """Retrieve a command from the registry."""
        version = version or self._default_version
        return self._commands[version][command_name]
