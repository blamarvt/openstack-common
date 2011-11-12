from .datatypes import Boolean
from .datatypes import Class
from .datatypes import Integer
from .datatypes import String
from .registry import ConfigRegistry


# Easy-access configuration methods
add_option = ConfigRegistry.add_option  # pylint: disable=C0103
get_section = ConfigRegistry.get_section  # pylint: disable=C0103
