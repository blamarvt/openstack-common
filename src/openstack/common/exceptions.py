class ExceptionWithMessage(Exception):
    """Base exception which has a message."""

    def __init__(self, **kwargs):
        """Initialize exception with keyword arguments."""
        Exception.__init__(self)
        self.message = self.message % kwargs


class NoSuchConfigOption(ExceptionWithMessage):
    message = _("No option '%(option)s' defined for config "
                "section '%(section)s'.")
