"""Decorator for converting assertion errors into broken-test errors."""

from collections.abc import Callable
from functools import wraps

from allure import attach, attachment_type

from automation.custom.logger.project_logger import logger
from automation.web_playwright_custom.pages.base_pw.custom_errors import BrokenTestError
from automation.web_playwright_custom.pages.base_pw.utils.extract_page_from_args import _extract_page_from_args


def business_check_to_broken[**P, RET](func: Callable[P, RET]) -> Callable[P, RET]:
    """Convert AssertionError into BrokenTestError and attach a page screenshot.

    Args:
        func: Function to decorate.

    Notes:
        Playwright's expect() raises AssertionError when an assertion fails.
        This decorator converts that exception into BrokenTestError so that Allure
        can report the test as broken rather than failed.
        Use this decorator only for assertions whose failures should be classified
        as test or infrastructure issues, not product defects.

    Returns:
        A wrapped function that converts AssertionError into BrokenTestError.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> RET:
        """Execute the function and convert AssertionError into BrokenTestError."""
        try:
            return func(*args, **kwargs)
        except AssertionError as error:
            page = _extract_page_from_args(args=args)

            if page is not None:
                try:
                    attach(
                        body=page.screenshot(),
                        name="Page state when assertion error was intercepted",
                        attachment_type=attachment_type.PNG,
                    )
                except Exception:
                    logger.exception("Failed to attach a page screenshot to the Allure report.")

            raise BrokenTestError(str(error)) from error

    return wrapper
