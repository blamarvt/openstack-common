import collections

import openstack.common.config.datatypes as config_types
import openstack.common.exceptions as exceptions


class Registry(object):
    """Command registry."""

    def __init__(self, config):
        """Initialize a new registry."""
        section = "command_registry"
        self._commands = collections.defaultdict(dict)

    def add(self, command_cls):
        """Register a new command with the registry."""
        version = command_cls.version
        name = command_cls.__name__
        self._commands[version][name] = command_cls

    def get(self, command_name, version=None):
        """Retrieve a command from the registry."""
        try:
            return self._commands[version][command_name]
        except KeyError:
            raise exceptions.NoSuchCommand(version=version, name=command_name)


class Command(object):
    """Basic command to be executed."""
    version = 1

    def __call__(self):
        """Execute this command."""
        pass
