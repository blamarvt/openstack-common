import collections
import Queue

import openstack.common.config.datatypes as config_types
import openstack.common.exceptions as exceptions


class Registry(object):
    """Command registry."""

    def __init__(self):
        """Initialize a new registry."""
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


class EchoCommand(object):
    """Command which echos it's input."""
    version = 1

    def __init__(self, *args, **kwargs):
        """Initialize the echo command."""
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        """Execute this command."""
        return self.args, self.kwargs


class SimpleQueuingStrategy(object):
    """Simple queuing strategy for remote command handling.

    Just as a note, this is NOT a valid strategy for any sort of deplyment
    and is meant to illustrate the strategy interface.
    """

    def __init__(self):
        """Initialize the queuing strategy."""
        hosts = collections.defaultdict
        services = lambda: collections.defaultdict(Queue.Queue)
        self._queues = hosts(services)

    def send(self, command, service, host):
        """Send a command to another service on a particular host."""
        self._queues[host][service].put_nowait(command)

    def recv(self, service, host):
        """Recieve a command from another service."""
        return self._queues[host][service].get_nowait()


class RemoteCommand(object):
    """Sends and recieves remote commands."""

    default_strategy = SimpleQueuingStrategy

    def __init__(self, config):
        """Initialize a new remote command object."""
        section = "remote_command"
        config.define(section=section,
                      name="strategy",
                      datatype=config_types.Class,
                      default=self.default_strategy,
                      description="The strategy to use when dealing with "
                                  "remote commands.")
        self._strategy = config.get(section, "strategy")()

    def send(self, command, service, host):
        """Send a command to another service on a particular host."""
        self._strategy.send(command, service, host)

    def recv(self, service, host):
        """Recieve a command from another service."""
        return self._strategy.recv(service, host)
