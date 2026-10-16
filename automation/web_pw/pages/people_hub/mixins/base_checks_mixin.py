"""Module providing common assertions and element checks for PeopleHub Page Objects."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Literal

from playwright.sync_api import Locator, TimeoutError

from automation.custom.allure_custom.custom_allure import step
from automation.custom.asserts.soft_assert import soft_assert
from automation.web_playwright_custom.pages.base_pw import PlaywrightLocator, get_description
from automation.web_pw.pages.people_hub.constants import TIME_ACTION, TIME_LOAD, TIME_WAIT
from automation.web_pw.pages.people_hub.utils.make_screenshot import make_screenshot

if TYPE_CHECKING:
    from automation.web_playwright_custom.pages.base_pw import BasePagePW

    class _Base(BasePagePW):
        """Base class for static type analysis."""

else:

    class _Base:
        """Base class for runtime execution."""


class BaseChecksMixin(_Base):
    """Mixin providing reusable checks for PeopleHub Page Objects."""

    @step(title="Get locator by text")
    def get_by_text(
        self,
        text: str,
        exact: bool = False,
    ) -> PlaywrightLocator:
        """Get a custom locator by text and attach a readable description.

        Args:
            text: Text to search for.
            exact: Whether the text must match exactly.

        Returns:
            A custom locator with a descriptive label.
        """

        locator = self.page.get_by_text(text=text, exact=exact)

        return locator.describe(description=f'Element with text "{text}"')

    @step(title="Wait for element to become visible")
    @make_screenshot
    def expect_to_be_visible(
        self,
        locator: PlaywrightLocator | Locator,
        timeout: float = TIME_LOAD,
        is_need_scroll: bool = False,
    ):
        """Wait until an element becomes visible.

        Args:
            locator: Element locator.
            timeout: Maximum wait time in milliseconds.
            is_need_scroll: Whether to scroll the element into view before checking.
        """

        if is_need_scroll:
            self._scroll_into_view(locator=locator, timeout=timeout)

        self.expect(target=locator).to_be_visible(timeout=timeout)

    @step(title="Wait for all elements to become visible")
    @make_screenshot
    def expect_all_to_be_visible(
        self,
        locators: Iterable[PlaywrightLocator | Locator],
        timeout: float = TIME_WAIT,
        is_need_scroll: bool = False,
    ):
        """Wait until every supplied element becomes visible.

        Args:
            locators: Iterable of element locators.
            timeout: Maximum wait time for each element, in milliseconds.
            is_need_scroll: Whether to scroll each element into view before checking.
        """

        for locator in locators:
            self.expect_to_be_visible(
                locator=locator,
                timeout=timeout,
                is_need_scroll=is_need_scroll,
            )

    @step(title="Soft-check element visibility")
    def soft_check_elements_visibility(
        self,
        locators: Iterable[PlaywrightLocator],
        is_visible: bool = True,
        timeout: float = TIME_ACTION,
        is_need_scroll: bool = False,
    ):
        """Soft-check the visibility state of multiple elements.

        Args:
            locators: Iterable of element locators.
            is_visible: Expected visibility state.
            timeout: Maximum wait time for each element, in milliseconds.
            is_need_scroll: Whether to scroll visible elements into view before checking.

        Raises:
            ValueError: If no locators are supplied.
        """

        locators_list = list(locators)

        if not locators_list:
            raise ValueError("No locators were provided for the visibility check.")

        for locator in locators_list:
            self.soft_check_visibility(
                locator=locator,
                is_visible=is_visible,
                timeout=timeout,
                is_need_scroll=is_need_scroll,
            )

    @step(title="Soft-check element visibility")
    def soft_check_visibility(
        self,
        locator: PlaywrightLocator | Locator,
        is_visible: bool = True,
        timeout: float = TIME_ACTION,
        message: str | None = None,
        is_need_scroll: bool = False,
    ):
        """Soft-check whether an element is visible or hidden.

        Args:
            locator: Element locator.
            is_visible: Expected visibility state.
            timeout: Maximum wait time in milliseconds.
            message: Optional custom failure message.
            is_need_scroll: Whether to scroll the element into view before checking visibility.

        """

        if is_need_scroll and is_visible:
            self._scroll_into_view(locator=locator, timeout=timeout)

        try:
            if is_visible:
                self.expect(target=locator).to_be_visible(timeout=timeout)
            else:
                self.expect(target=locator).to_be_hidden(timeout=timeout)

            condition = True
        except (TimeoutError, AssertionError):
            condition = False

        expected_state = "visible" if is_visible else "hidden"
        failure_message = message or (
            f"Element {get_description(target=locator)} was not {expected_state}."
        )

        soft_assert(condition=condition, message=failure_message)

    @step(title="Check element visibility")
    def check_visibility(
        self,
        locator: PlaywrightLocator,
        is_visible: bool = True,
        timeout: float = TIME_WAIT,
        is_need_scroll: bool = False,
    ):
        """Strictly check whether an element is visible or hidden.

        Args:
            locator: Element locator.
            is_visible: Expected visibility state.
            timeout: Maximum wait time in milliseconds.
            is_need_scroll: Whether to scroll the element into view before checking visibility.
        """

        if is_need_scroll and is_visible:
            self._scroll_into_view(locator=locator, timeout=timeout)

        state: Literal["visible", "hidden"] = "visible" if is_visible else "hidden"
        locator.wait_for(state=state, timeout=timeout)

    @staticmethod
    def _scroll_into_view(
        locator: PlaywrightLocator | Locator,
        timeout: float = TIME_ACTION,
    ):
        """Scroll an element into the visible viewport area.

        Args:
            locator: Element locator.
            timeout: Maximum wait time in milliseconds.

        Raises:
            TimeoutError: If the element cannot be scrolled into view within the timeout.
        """

        locator.scroll_into_view_if_needed(timeout=timeout)

    @step(title="Soft-check element text")
    def soft_check_text(
        self,
        expected_text: str,
        locator: PlaywrightLocator,
        timeout: float = TIME_ACTION,
        **kwargs: Any,
    ):
        """Soft-check the text content of an element.

        Args:
            expected_text: Expected text content.
            locator: Element locator.
            timeout: Maximum wait time in milliseconds.
            **kwargs: Additional supported arguments for Playwright's to_have_text assertion.
        """

        try:
            self.expect(target=locator).to_have_text(
                expected=expected_text,
                timeout=timeout,
                **kwargs,
            )
            condition = True
        except (TimeoutError, AssertionError):
            condition = False

        soft_assert(
            condition=condition,
            message=f'Element {get_description(target=locator)} did not contain the expected text "{expected_text}".',
        )

    @step(title='Soft-check attribute "{name}"')
    def soft_check_attribute_value(
        self,
        locator: PlaywrightLocator,
        name: str,
        expected_value: str,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check an element's attribute value.

        Args:
            locator: Element locator.
            name: Attribute name.
            expected_value: Expected attribute value.
            timeout: Maximum wait time in milliseconds.
        """

        try:
            locator.wait_for(state="attached", timeout=timeout)
            actual_value = locator.get_attribute(name=name)
            condition = actual_value == expected_value
            message = (
                f'Attribute "{name}" had value "{actual_value}", '
                f'but expected "{expected_value}".'
            )
        except TimeoutError:
            condition = False
            message = f"Element {get_description(target=locator)} was not attached to the DOM."

        soft_assert(condition=condition, message=message)

    @step(title="Soft-check checkbox or radio state")
    def soft_check_checked(
        self,
        locator: PlaywrightLocator,
        is_checked: bool = True,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check whether a checkbox or radio button is checked.

        Args:
            locator: Element locator.
            is_checked: Expected checked state.
            timeout: Maximum wait time in milliseconds.
        """

        try:
            actual_state = locator.is_checked(timeout=timeout)
            condition = actual_state == is_checked

        except TimeoutError:
            condition = False

        expected_state = "checked" if is_checked else "unchecked"
        message = f"Element {get_description(target=locator)} was not {expected_state}."

        soft_assert(condition=condition, message=message)

    @step(title='Check whether the current URL contains "{url_part}"')
    def check_current_url_contains(self, url_part: str):
        """Check whether the current page URL contains the expected substring.

        Args:
            url_part: Expected substring of the current URL.
        """

        url = self.page.url

        assert url_part in url, f'Current URL "{url}" does not contain "{url_part}".'

    @step(title="Soft-check that an element is absent from the DOM")
    def soft_check_element_not_exist(
        self,
        locator: PlaywrightLocator,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check that no elements match the locator.

        Args:
            locator: Element locator.
            timeout: Maximum wait time in milliseconds.
        """

        try:
            self.expect(target=locator).to_have_count(count=0, timeout=timeout)
            condition = True

        except (TimeoutError, AssertionError):
            condition = False

        message = f"Element {get_description(target=locator)} is present in the DOM."

        soft_assert(condition=condition, message=message)

    @step(title="Soft-check element enabled state")
    def soft_check_element_enabled(
        self,
        locator: PlaywrightLocator,
        is_enabled: bool = True,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check whether an element is enabled or disabled.

        Args:
            locator: Element locator.
            is_enabled: Expected enabled state.
            timeout: Maximum wait time in milliseconds.
        """

        try:
            if is_enabled:
                self.expect(target=locator).to_be_enabled(timeout=timeout)

            else:
                self.expect(target=locator).to_be_disabled(timeout=timeout)

            condition = True

        except (TimeoutError, AssertionError):
            condition = False

        message = (
            f"Element {get_description(target=locator)} did not match "
            f"expected enabled={is_enabled}."
        )

        soft_assert(condition=condition, message=message)

    @step(title="Soft-check element count")
    def soft_check_elements_count(
        self,
        locator: PlaywrightLocator,
        expected_count: int,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check the number of elements matching a locator.

        Args:
            locator: Element locator.
            expected_count: Expected number of matching elements.
            timeout: Maximum wait time in milliseconds.

        Raises:
            ValueError: If the expected count is negative.
        """

        if expected_count < 0:
            raise ValueError("Expected element count must not be negative.")

        try:
            self.expect(target=locator).to_have_count(count=expected_count, timeout=timeout)
            condition = True
        except (TimeoutError, AssertionError):
            condition = False

        message = (
            f"Element count for {get_description(target=locator)} "
            f"did not match the expected count of {expected_count}."
        )

        soft_assert(condition=condition, message=message)

    @step(title='Soft-check CSS property "{property_name}"')
    def soft_check_css_property(
        self,
        locator: PlaywrightLocator,
        property_name: str,
        expected_value: str,
        timeout: float = TIME_ACTION,
    ):
        """Soft-check a computed CSS property value.

        Args:
            locator: Element locator.
            property_name: CSS property name.
            expected_value: Expected computed CSS value.
            timeout: Maximum wait time in milliseconds.
        """

        try:
            locator.wait_for(state="attached", timeout=timeout)
            actual_value = locator.evaluate(
                expression="(el, propertyName) => window.getComputedStyle(el).getPropertyValue(propertyName)",
                arg=property_name,
            )
            condition = actual_value == expected_value
            message = (
                f'CSS property "{property_name}" had value "{actual_value}", '
                f'but expected "{expected_value}".'
            )
        except TimeoutError:
            condition = False
            message = f"Element {get_description(target=locator)} was not attached to the DOM."

        soft_assert(condition=condition, message=message)