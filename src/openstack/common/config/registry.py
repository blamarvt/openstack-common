import collections
import ConfigParser
import os

import openstack.common.exceptions as exceptions


class ConfigRegistry(object):
    """Used to store and retrieve config values."""

    parser = None
    app_name = "openstack-common"

    search_dirs = [
        "~/.%(app_name)s",
        "~",
        "/etc/%(app_name)s",
        "/etc",
    ]

    _registry = collections.defaultdict(dict)
    _filename = "%(app_name)s.conf"

    class ConfigSection(object):
        """Used to pass around a specific section of the registry."""

        def __init__(self, section_name):
            """Initialize and check to make sure the section exists."""
            self._section_name = section_name

        def get(self, option_name):
            """Get the value of a particular config option."""
            section_name = self._section_name
            section = ConfigRegistry._registry[section_name]
            (value, datatype) = section.get(option_name, (None, None))
            if value is None and datatype is None:
                raise exceptions.NoSuchConfigOption(option_name=option_name,
                                                    section_name=section_name)
            return datatype.format_value(value)

    @staticmethod
    def create_parser():
        """Create and return a new parser (stubout point)."""
        return ConfigParser.ConfigParser()

    @classmethod
    def find_config_file(cls):
        """Attempt to locate a configuration file."""
        config_file_name = cls._filename % ConfigRegistry.__dict__

        for directory in cls.search_dirs:
            directory = directory % ConfigRegistry.__dict__
            full_path = os.path.join(directory, config_file_name)
            clean_path = os.path.abspath(os.path.expanduser(full_path))
            if os.path.exists(clean_path):
                return clean_path

    @classmethod
    def load_from_path(cls, path):
        """Initialize the registry from a particular path."""
        cls.load_from_filelike(open(path))

    @classmethod
    def load_from_filelike(cls, filelike):
        """Initialize the registry from a filelike object."""
        cls.parser = cls.create_parser()
        cls.parser.readfp(filelike)

    @classmethod
    def add_option(cls, section, name, datatype, default, description):
        """Add a configuration object to the global config registry.

        :param section: The config section this option belongs in
        :param name: The name of the config option
        :param datatype: The class/datatype of the config option
        :param default: The default value for the config option
        :param description: A short description of the config option
        :returns: None

        """
        cls._registry[section][name] = (default, datatype)

    @classmethod
    def get_section(cls, section_name):
        """Retrieve a section from the registry, if possible."""
        return cls.ConfigSection(section_name)

    @classmethod
    def get(cls, section_name, option_name):
        """Retrieve an option value from the registry, if possible."""
        section = cls.get_section(section_name)
        return section.get(option_name)


config_path = ConfigRegistry.find_config_file()
if config_path is not None:
    ConfigRegistry.load_from_path(config_path)
else:
    ConfigRegistry.parser = ConfigRegistry.create_parser()
