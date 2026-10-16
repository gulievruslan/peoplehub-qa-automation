
"""Base class for Playwright web element locators."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Never, NoReturn

from playwright.sync_api import Locator, Page


class LocatorPW:
    """Base class for Playwright web element locators.

    Attributes:
        name: Element description.
        selector: String selector (CSS/XPath).
        locator_fn: Callable that accepts a page and returns a Locator.
    """

    def __init__(
        self,
        name: str,
        selector: str | None = None,
        locator_fn: Callable[[Page], Locator] | None = None,
        page: Page | None = None,
    ) -> None:
        """Initialize the locator object."""
        self.name = name

        if (selector is not None) == (locator_fn is not None):
            raise ValueError(
                "Exactly one of 'selector' or 'locator_fn' must be provided. "
                f"Received: {selector=} {locator_fn=}",
            )

        self.selector = selector
        self.locator_fn = locator_fn
        self._page = page
        self._cached_locator: Locator | None = None
        self._cached_page: Page | None = None
        self._attr_name: str | None = None
        self._owner: type[object] | None = None

    def get_locator(self, page: Page) -> Locator:
        """Get the Playwright Locator."""
        if self.locator_fn is not None:
            return self.locator_fn(page)

        if self.selector is not None:
            return page.locator(self.selector)

        raise TypeError("The locator must be defined by either a selector or a callable.")

    def format(self, **kwargs: object) -> LocatorPW:
        """Format a string-based locator."""
        if self.selector is None:
            raise TypeError("A locator created with locator_fn cannot be formatted.")

        return LocatorPW(
            name=self.name.format(**kwargs),
            selector=self.selector.format(**kwargs),
            page=self._page,
        )

    def __getattr__(self, item: str) -> Any:
        """Delegate attribute access to the underlying Locator."""
        if self._page is None:
            raise AttributeError(
                f'"{type(self).__name__}" is not bound to a page and has no attribute "{item}".',
            )

        if self._cached_locator is None or self._cached_page is not self._page:
            self._cached_locator = self.get_locator(page=self._page)
            self._cached_page = self._page

        return getattr(self._cached_locator, item)

    def __repr__(self) -> str:
        """Return the object's developer-friendly string representation."""
        selector_part = f"selector={self.selector!r}" if self.selector else "locator_fn=<callable>"
        page_state = "bound" if self._page is not None else "None"

        return f"{type(self).__name__}(name={self.name!r}, {selector_part}, page={page_state})"

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        locator_type = f'selector="{self.selector}"' if self.selector else "callable locator"

        return f'Element "name={self.name!r}" using {locator_type}'

    def __set_name__(self, owner: type[object], name: str) -> None:
        """Store the attribute name when the locator is declared on a class."""
        self._attr_name = name
        self._owner = owner

    def __get__(
        self,
        instance: object | None,
        owner: type[object],
    ) -> LocatorPW:
        """Bind the locator to the page object when accessed through an instance."""
        if instance is None:
            return self

        page = getattr(instance, "page", None)

        if page is None:
            raise AttributeError(
                f'LocatorPW "{self.name}" requires a "page" attribute on '
                f"{type(instance).__name__}.",
            )

        if not isinstance(page, Page):
            raise TypeError(
                f'Expected "page" to be a Playwright Page, got {type(page).__name__}.',
            )

        if self._page is not page:
            self._page = page
            self._cached_locator = None
            self._cached_page = None

        return self

    def __set__(self, instance: object, value: Never) -> NoReturn:
        """Prevent the locator descriptor from being overwritten on an instance."""
        raise AttributeError(
            f'Cannot overwrite LocatorPW "{self._attr_name}". '
            "Use formatting instead: .format(param=value).",
        )


type PlaywrightLocator = LocatorPW | Locator
