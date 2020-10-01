# -*- coding: utf-8 -*-


class EclyssiaException(Exception):
    """Allows to catch any Eclyssia Exception"""


class Forbidden(EclyssiaException):
    """Forbidden Exception such as a 404"""


class NotFound(EclyssiaException):
    pass


class InvalidEndPoint(EclyssiaException):
    pass
