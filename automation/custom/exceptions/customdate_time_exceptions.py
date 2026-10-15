"""Exceptions raised by the CustomDateTime utilities."""


class CustomDateTimeError(Exception):
    """Base exception for CustomDateTime-related errors."""


class CustomDateTimeWrongInputError(CustomDateTimeError):
    """Raised when an unsupported input value is provided."""


class CustomDateTimeMaskError(CustomDateTimeError):
    """Raised when a date string cannot be parsed using the supplied format."""
