

class ControllerException(Exception):
    pass


class ArgumentException(Exception):
    def __init__(self, message):
        self.msg = message


class NotFoundException(ArgumentException):
    pass


class MissingException(ArgumentException):
    pass

