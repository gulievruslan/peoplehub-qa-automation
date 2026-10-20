"""Module containing basic interaction methods for Page Objects."""
from allure import step
from playwright.sync_api import Locator, Page, Position

from automation.web_playwright_custom.pages.base_pw import LocatorPW, PlaywrightLocator
from automation.web_pw.pages.people_hub.constants import TIME_ACTION
from automation.web_pw.pages.people_hub.custom_types import Button, SelectorChain, SelectorStep


class BaseActionsMixin:
    """Mixin providing basic interaction methods."""

    page: Page

    @step(title="Get text from element")
    def get_text_from_element(self, locator: PlaywrightLocator, timeout: float = TIME_ACTION) -> str:
        """Get the visible text of an element.

        Args:
            locator: Element locator.
            timeout: Timeout in milliseconds.

        Raises:
            ValueError: If the element contains no non-whitespace text.

        Returns:
            The visible text of the element.
        """

        text = locator.inner_text(timeout=timeout)

        if not text.strip():
            raise ValueError(f"No text found in element with locator: {locator}")

        return text

    @step(title="Get elements by visibility: {is_visible}")
    def get_visible_elements(
        self,
        locator: PlaywrightLocator,
        is_visible: bool = True,
    ) -> list[Locator]:
        """Get matching visible or hidden elements.

        Args:
            locator: Locator identifying the elements.
            is_visible: Whether to select visible or hidden elements.

        Returns:
            A list of Playwright locators matching the visibility condition.
        """

        return locator.filter(visible=is_visible).all()

    @step(title="Hover over element")
    def hover_element(
        self,
        locator: PlaywrightLocator,
        x_offset: int = 0,
        y_offset: int = 0,
        timeout: float = TIME_ACTION,
    ):
        """Hover over an element, optionally offset from its center.

        Args:
            locator: Element to hover over.
            x_offset: Horizontal offset from the element's center, in pixels.
            y_offset: Vertical offset from the element's center, in pixels.
            timeout: Maximum time to wait for the action, in milliseconds.

        Raises:
            ValueError: If offsets are requested but the element's bounding box is unavailable.
        """
        position: Position | None = None

        if x_offset or y_offset:
            bounding_box = locator.bounding_box(timeout=timeout)
            if bounding_box is None:
                raise ValueError(f"Cannot determine the bounding box for locator: {locator}")

            position = {
                "x": bounding_box["width"] / 2 + x_offset,
                "y": bounding_box["height"] / 2 + y_offset,
            }

        locator.hover(timeout=timeout, position=position)

    @step(title="Clear field and type text sequentially")
    def clear_and_type_like_user(
        self,
        locator: PlaywrightLocator,
        value: str = "",
        is_clear: bool = True,
        timeout: float = TIME_ACTION,
    ):
        """Optionally clear an input and type text character by character.

        Args:
            locator: Input locator.
            value: Text to enter.
            is_clear: Whether to clear the input before typing.
            timeout: Timeout in milliseconds.
        """
        if is_clear:
            locator.fill("", timeout=timeout)

        if value:
            locator.press_sequentially(value, timeout=timeout)

    @step(title="Press key on element")
    def press_key_on_element(
        self,
        locator: PlaywrightLocator,
        key: str,
        timeout: float = TIME_ACTION,
    ):
        """Press a keyboard key while the element is focused.

        Args:
            locator: Element locator.
            key: Key to press, such as "Enter", "Tab", or "Escape".
            timeout: Timeout in milliseconds.
        """

        locator.press(key=key, timeout=timeout)

    def click_on_button(self, button: Button):
        """Click a button using its description.

        Locator priority:
            1. data-testid, if provided.
            2. Button role and accessible name, if exactly one match exists.
            3. Exact text as a fallback, if exactly one match exists.

        Args:
            button: Button description with a name and optional data_testid.

        Raises:
            ValueError: If the fallback search finds zero or multiple matches.
        """

        with step(title=f'Click button "{button.name}"'):
            if button.data_testid:
                locator_button = self.page.get_by_test_id(
                    test_id=button.data_testid,
                )
            else:
                role_locator = self.page.get_by_role(role="button", name=button.name)
                count = role_locator.count()

                if count == 1:
                    locator_button = role_locator
                elif count > 1:
                    raise ValueError(
                        f'Button "{button.name}" matched {count} elements. '
                        "Provide data_testid or use click_on_element with a specific context."
                    )
                else:
                    text_locator = self.page.get_by_text(text=button.name, exact=True)
                    text_count = text_locator.count()

                    if text_count != 1:
                        raise ValueError(
                            f'Exact text "{button.name}" matched {text_count} elements. '
                            "Provide data_testid or use a more specific locator."
                        )

                    locator_button = text_locator

            locator_button.describe(description=f'Button "{button.name}"').click(timeout=TIME_ACTION)

    @step("Click element: {description}")
    def click_on_element(
        self,
        selector: SelectorChain | PlaywrightLocator,
        is_force: bool = False,
        description: str = "",
    ):
        """Click an element identified by a selector chain or locator.

        Args:
            selector: Selector chain or locator.
            is_force: force bool parameter
            description: element description.
        """
        locator = selector if isinstance(selector, (LocatorPW, Locator)) else self._build_locator(selector)
        desc = description or getattr(selector, "name", str(selector))
        locator.describe(description=desc).click(force=is_force, timeout=TIME_ACTION)

    def _build_locator(self, selector: SelectorChain) -> Locator:
        """Build a Playwright locator from a simple or nested selector chain.

        Args:
            selector: A simple selector or a nested selector chain.

        Returns:
            The resolved Playwright locator.
        """

        return self._build_locator_in_context(self.page, selector)

    def _build_locator_in_context(
        self,
        context: Locator | Page,
        selector: SelectorChain,
    ) -> Locator:
        """Resolve a selector chain relative to an existing context.

        Args:
            context: Page or parent locator used as the search context.
            selector: A simple selector or a nested selector chain.

        Returns:
            The resolved Playwright locator.
        """

        if isinstance(selector, SelectorStep):
            return self._apply_step(context, selector)

        parent_locator = self._build_locator_in_context(context, selector.parent)

        return self._build_locator_in_context(parent_locator, selector.child)

    @staticmethod
    def _apply_step(context: Locator | Page, step_item: SelectorStep) -> Locator:
        """Apply a single selector step to the search context.

        Args:
            context: Page or locator used as the search context.
            step_item: Selector step containing the search strategy and value.

        Returns:
            The resulting Playwright locator.

        Raises:
            ValueError: If the selector strategy is not supported.
        """

        match step_item.by:
            case "testid":
                locator = context.get_by_test_id(step_item.value)
            case "text":
                locator = context.get_by_text(step_item.value)
            case "css":
                locator = context.locator(step_item.value)
            case _:
                raise ValueError(f"Unsupported selector strategy: {step_item.by}")

        if step_item.nth is not None:
            return locator.nth(step_item.nth)

        return locator
