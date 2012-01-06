class Datatype(object):

    _default = None

    def __init__(self, name, description, default=None):
        self.name = name
        self.description = description
        self.value = default or self._default

    def from_parser(self, parser):
        pass


class Integer(Datatype):
    _default = 0


class String(Datatype):
    _default = ""


class Class(Datatype):
    _default = None


class Boolean(Datatype):
    _default = None
