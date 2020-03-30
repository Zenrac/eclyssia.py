# -*- coding: utf-8 -*-


class EclyssiaException(Exception):
    """Allows to catch any Eclyssia Exception"""


class Forbidden(EclyssiaException):
    pass


class NotFound(EclyssiaException):
    pass


class InvalidEndPoint(EclyssiaException):
    pass
