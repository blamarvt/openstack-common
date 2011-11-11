import os

class ConfigRegistry(object):
    """Used to store and retrieve config values."""

    _parser = None
    _app_name = None
    _filename = "%(app_name)s.conf"
    _expand_path = lambda path: os.path.abspath(os.path.expanduser(path))
    _search_dirs = map(_expand_path, [
        "~/.%(app_name)s",
        "~",
        "/etc/%(app_name)s",
        "/etc",
    ])

    @classmethod
    def find_config_file(cls):
        """Attempt to locate a configuration file."""
        for directory in cls.search_dirs:
            full_path = os.path.join(directory, cls._filename) % locals()
            if os.path.exists(full_path):
                return full_path

    @classmethod
    def load_from_path(cls, path):
        cls.load_from_filelike(open(path))

    @classmethod
    def load_from_filelike(cls, filelike):
        cls.parser = ConfigParser.ConfigParser()
        cls.parser.readfp(filelike)

    @classmethod
    def add_option(cls, name, datatype, default, section, description):
        """Add a configuration object to the global config registry.

        :param name: The name of the config option
        :param datatype: The class/datatype of the config option
        :param default: The default value for the config option
        :param description: A short description of the config option
        :returns: None

        """
        pass

    @classmethod
    def get_section(cls, section_name):
        return cls.
