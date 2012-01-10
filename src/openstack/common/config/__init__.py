import os

from .datatypes import Boolean
from .datatypes import Class
from .datatypes import Integer
from .datatypes import Object
from .datatypes import String
from .registry import Registry


# Global registry
#REGISTRY = Registry()


# Easy-access configuration methods
#define = REGISTRY.define  # pylint: disable=C0103
#get = REGISTRY.get  # pylint: disable=C0103
#set = REGISTRY.set  # pylint: disable=C0103


def find_config(app_name):
    """Find a configuration file given an application name."""
    filename = "%s.conf" % app_name
    search_dirs = [
        "~/.%s" % app_name,
        "~",
        "/etc/%s" % app_name,
        "/etc",
    ]

    for directory in search_dirs:
        path = os.path.join(directory, filename)
        path = os.path.abspath(os.path.expanduser(path))
        if os.path.exists(path):
            return path
