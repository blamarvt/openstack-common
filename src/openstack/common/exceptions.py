class ExceptionWithMessage(Exception):
    """Base exception which has a message."""

    def __init__(self, **kwargs):
        """Initialize exception with keyword arguments."""
        self.message = self.message % kwargs


class NoSuchConfigOption(ExceptionWithMessage):
    message = _("No option '%(option_name)s' defined for config "
                "section '%(section_name)s'.")
