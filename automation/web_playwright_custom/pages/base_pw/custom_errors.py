"""Exceptions."""


class BrokenTestError(Exception):
    """Exception indicating a test infrastructure or assertion issue rather than a product defect.

    Notes:
        This class is used to convert AssertionError into BrokenTestError so that Allure
        reports the test status as "broken" (yellow) instead of "failed" (red).

        BrokenTestError indicates an issue with the test itself (an incorrect expect,
        a UI change, or an exceeded wait timeout), rather than a product defect.
    """