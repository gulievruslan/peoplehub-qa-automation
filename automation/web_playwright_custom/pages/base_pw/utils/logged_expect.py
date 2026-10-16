"""Utility for logging Playwright assertions."""

from typing import Any, overload

from playwright.sync_api import APIResponse, Locator, Page, expect

from automation.web_playwright_custom.pages.base_pw.locators.locators import LocatorPW
from automation.web_playwright_custom.pages.base_pw.utils import _auto_patch_logging
from automation.web_playwright_custom.pages.base_pw.utils.get_description import get_description


@overload
def _logged_expect(target: Locator, description: str | None = None) -> Any: ...


@overload
def _logged_expect(target: LocatorPW, description: str | None = None) -> Any: ...


@overload
def _logged_expect(target: Page, description: str | None = None) -> Any: ...


@overload
def _logged_expect(target: APIResponse, description: str | None = None) -> Any: ...


def _logged_expect(
    target: Locator | LocatorPW | Page | APIResponse,
    description: str | None = None,
) -> Any:
    """Wrap expect() and automatically log assertion calls.

    Args:
        target: Object to assert against.
        description: Optional description of the target.

    Returns:
        The Playwright assertion object with logging enabled.
    """

    description = get_description(target=target, description=description)

    if isinstance(target, LocatorPW):
        page = target.page

        if page is None:
            raise ValueError(f'LocatorPW "{target.name}" is not bound to a page.')

        target = target.get_locator(page=page)

    assertions_obj = expect(target)
    _auto_patch_logging(obj=assertions_obj, log_prefix=f"expect({description})")

    return assertions_obj
