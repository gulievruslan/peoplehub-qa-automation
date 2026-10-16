"""Module providing explicit waits for UI elements and pages."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal

from playwright.sync_api import TimeoutError

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.constants import TIME_ACTION

if TYPE_CHECKING:
    from automation.web_playwright_custom.pages.base_pw import BasePagePW, PlaywrightLocator


    class _Base(BasePagePW):
        """Base class used for static type checking."""

else:

    class _Base:
        """Runtime base class for the mixin."""


class WaiterActionsMixin(_Base):
    """Reusable explicit waits for UI elements and pages."""

    @step(title="Check whether an element is visible")
    def is_element_visible(
        self,
        locator: PlaywrightLocator,
        timeout: float = TIME_ACTION,
    ) -> bool:
        """Return whether an element becomes visible within the timeout.

        Args:
            locator: Element to check.
            timeout: Maximum wait time in milliseconds.

        Returns:
            True if the element becomes visible; otherwise, False.
        """
        try:
            self.wait_for_element(locator=locator, state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False

    @step(title="Wait for an element to reach state {state}")
    def wait_for_element(
        self,
        locator: PlaywrightLocator,
        state: Literal["attached", "detached", "hidden", "visible"] = "visible",
        timeout: float = TIME_ACTION,
    ):
        """Wait until an element reaches the requested state.

        Args:
            locator: Element to wait for.
            state: Expected element state.
            timeout: Maximum wait time in milliseconds.

        Raises:
            TimeoutError: If the element does not reach the requested state in time.
        """
        locator.wait_for(state=state, timeout=timeout)

    @step(title="Wait for an element to become hidden")
    def wait_for_invisibility(
        self,
        locator: PlaywrightLocator,
        timeout: float = TIME_ACTION,
    ):
        """Wait until an element is hidden or detached from the DOM.

        Args:
            locator: Element to wait for.
            timeout: Maximum wait time in milliseconds.
        """
        self.expect(target=locator).to_be_hidden(timeout=timeout)

    @step(title="Wait for an element to appear and disappear")
    def wait_for_element_appear_and_disappear(
        self,
        locator: PlaywrightLocator,
        timeout: float = TIME_ACTION,
    ):
        """Wait for an element to become visible and then hidden.

        Each phase receives the specified timeout.

        Args:
            locator: Element to wait for.
            timeout: Maximum wait time in milliseconds for each phase.
        """
        self.wait_for_element(locator=locator, state="visible", timeout=timeout)
        self.wait_for_invisibility(locator=locator, timeout=timeout)

    @step(title='Wait for URL to contain "{url_part}"')
    def wait_for_url_to_contain(
        self,
        url_part: str,
        timeout: float = TIME_ACTION,
    ):
        """Wait until the current URL contains a literal substring.

        Args:
            url_part: Literal substring expected in the URL.
            timeout: Maximum wait time in milliseconds.
        """
        if not url_part:
            raise ValueError("The URL fragment must not be empty.")

        self.page.wait_for_url(url=re.compile(re.escape(url_part)), timeout=timeout)

    @step(title="Wait for page load state {state}")
    def wait_for_page_load(
        self,
        state: Literal["domcontentloaded", "load", "networkidle"] = "load",
        timeout: float = TIME_ACTION,
    ):
        """Wait for the page to reach a specified load state.

        Args:
            state: Page lifecycle state to wait for.
            timeout: Maximum wait time in milliseconds.
        """
        self.page.wait_for_load_state(state=state, timeout=timeout)

    @step(title='Wait for text "{expected_text}" in an element')
    def wait_for_text_in_element(
        self,
        locator: PlaywrightLocator,
        expected_text: str,
        timeout: float = TIME_ACTION,
        use_contain: bool = False,
    ):
        """Wait until an element contains or exactly matches the expected text.

        Args:
            locator: Element whose text is checked.
            expected_text: Expected text.
            timeout: Maximum wait time in milliseconds.
            use_contain: If True, check for contained text instead of an exact text match.
        """
        if use_contain:
            self.expect(target=locator).to_contain_text(expected=expected_text, timeout=timeout)
        else:
            self.expect(target=locator).to_have_text(expected=expected_text, timeout=timeout)

    @step(title='Wait for attribute "{name}" to have the expected value')
    def wait_for_attribute_value(
        self,
        locator: PlaywrightLocator,
        name: str,
        expected_value: str,
        timeout: float = TIME_ACTION,
    ):
        """Wait until an element has the expected attribute value.

        Args:
            locator: Element whose attribute is checked.
            name: Attribute name.
            expected_value: Expected attribute value.
            timeout: Maximum wait time in milliseconds.
        """
        self.expect(target=locator).to_have_attribute(name=name, value=expected_value, timeout=timeout)

    @step(title="Wait for the expected number of elements")
    def wait_for_elements_count(
        self,
        locator: PlaywrightLocator,
        expected_count: int,
        timeout: float = TIME_ACTION,
    ):
        """Wait until the locator matches the expected number of elements.

        Args:
            locator: Locator matching the elements to count.
            expected_count: Expected number of matching elements.
            timeout: Maximum wait time in milliseconds.
        """
        if expected_count < 0:
            raise ValueError("Expected element count must not be negative.")

        self.expect(target=locator).to_have_count(count=expected_count, timeout=timeout)

    @step(title="Wait for an element to become enabled or disabled")
    def wait_for_element_state(
        self,
        locator: PlaywrightLocator,
        is_enabled: bool = True,
        timeout: float = TIME_ACTION,
    ):
        """Wait until an element reaches the expected enabled state.

        Args:
            locator: Element whose state is checked.
            is_enabled: Expected state; True means enabled and False means disabled.
            timeout: Maximum wait time in milliseconds.
        """
        if is_enabled:
            self.expect(target=locator).to_be_enabled(timeout=timeout)
        else:
            self.expect(target=locator).to_be_disabled(timeout=timeout)

    @step(title="Wait for an element to have the expected value")
    def wait_for_element_value(
        self,
        locator: PlaywrightLocator,
        expected_value: str,
        timeout: float = TIME_ACTION,
    ):
        """Wait until an input element has the expected value.

        Args:
            locator: Input element to check.
            expected_value: Expected input value.
            timeout: Maximum wait time in milliseconds.
        """
        self.expect(target=locator).to_have_value(value=expected_value, timeout=timeout)

    @step(title="Wait for the exact URL")
    def wait_for_exact_url(
        self,
        expected_url: str,
        timeout: float = TIME_ACTION,
    ):
        """Wait until the current URL exactly matches the expected URL.

        Args:
            expected_url: Expected URL.
            timeout: Maximum wait time in milliseconds.
        """
        self.page.wait_for_url(url=expected_url, timeout=timeout)
