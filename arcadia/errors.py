# -*- coding: utf-8 -*-


class ArcadiaException(Exception):
    """Allows to catch any Arcadia Exception"""

class Forbidden(ArcadiaException):
    pass


class NotFound(ArcadiaException):
    pass


class InvalidEndPoint(ArcadiaException):
    pass
