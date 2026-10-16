
"""Base page class for working with Playwright."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from playwright.sync_api import APIResponse, Locator, Page

from automation.web_pw.pages.base import BasePage
from automation.web_playwright_custom.pages.base_pw.custom_types import LoggedObjects
from automation.web_playwright_custom.pages.base_pw.locators import LocatorPW
from automation.web_playwright_custom.pages.base_pw.utils import _auto_patch_logging, _logged_expect

if TYPE_CHECKING:
    from playwright.sync_api import APIResponseAssertions, LocatorAssertions, PageAssertions


class BasePagePW(BasePage):
    """Base page class for Playwright.

    Attributes:
        page: Playwright Page instance.
    """

    def __init__(self, page: Page, url: str | None = None) -> None:
        """Initialize the page object.

        Args:
            page: Playwright Page instance.
            url: Optional page URL.
        """
        super().__init__(page=page, url=url)
        _auto_patch_logging(obj=page, log_prefix="Page")
        original_locator = page.locator

        def logged_locator(*args: Any, **kwargs: Any) -> Locator:
            """Wrap locator creation with logging.

            Args:
                *args: Positional arguments.
                **kwargs: Keyword arguments.

            Returns:
                A Locator instance with logging enabled.
            """
            locator = original_locator(*args, **kwargs)
            _auto_patch_logging(obj=locator, log_prefix="Locator")
            return locator

        self.page: Page = page
        self.page.__setattr__("locator", logged_locator)

    @overload
    def expect(self, target: Locator, description: str | None = None) -> LocatorAssertions: ...

    @overload
    def expect(self, target: LocatorPW, description: str | None = None) -> LocatorAssertions: ...

    @overload
    def expect(self, target: Locator | LocatorPW, description: str | None = None) -> LocatorAssertions: ...

    @overload
    def expect(self, target: Page, description: str | None = None) -> PageAssertions: ...

    @overload
    def expect(self, target: APIResponse, description: str | None = None) -> APIResponseAssertions: ...

    def expect(self, target: LoggedObjects, description: str | None = None) -> Any:
        """Create a Playwright expectation for the given target."""
        if isinstance(target, LocatorPW):
            if description is None:
                description = str(target)
            target_inner = target.get_locator(page=self.page)
        else:
            target_inner = target

        if isinstance(target_inner, Locator):
            return _logged_expect(target=target_inner, description=description)

        if isinstance(target_inner, Page):
            return _logged_expect(target=target_inner, description=description)

        if isinstance(target_inner, APIResponse):
            return _logged_expect(target=target_inner, description=description)

        raise TypeError(f"Unsupported expectation target type: {type(target_inner).__name__}")
