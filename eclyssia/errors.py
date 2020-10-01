# -*- coding: utf-8 -*-


class EclyssiaException(Exception):
    """Allows to catch any Eclyssia Exception"""


class Forbidden(EclyssiaException):
    """Forbidden Exception such as a 404"""


class NotFound(EclyssiaException):
    """Exception when the specified endpoint is not found"""


class InvalidEndPoint(EclyssiaException):
    """Exception when the specified endpoint is invalid"""
