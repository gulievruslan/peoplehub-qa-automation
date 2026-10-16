
"""Base class for Playwright web element locators."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Never, NoReturn, TypeAlias

from playwright.sync_api import Locator

if TYPE_CHECKING:
    from automation.web_pw.pages.base import PagePW


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
        locator_fn: Callable[["PagePW"], Locator] | None = None,
        page: "PagePW | None" = None,
    ) -> None:
        """Initialize the locator object.

        Args:
            name: Element description.
            selector: String selector (CSS/XPath).
            locator_fn: Callable that accepts a page and returns a Locator.
            page: Playwright page object.

        Raises:
            ValueError: If neither locator type or both locator types are provided.
        """
        self.name: str = name

        if (selector is not None) == (locator_fn is not None):
            raise ValueError(
                "Exactly one of 'selector' or 'locator_fn' must be provided. "
                f"Received: {selector=} {locator_fn=}",
            )

        self.selector: str | None = selector
        self.locator_fn: Callable[["PagePW"], Locator] | None = locator_fn
        self._page: "PagePW | None" = page
        self._cached_locator: Locator | None = None
        self._cached_page: "PagePW | None" = None
        self._attr_name: str | None = None
        self._owner: type["PagePW"] | None = None

    def get_locator(self, page: "PagePW") -> Locator:
        """Get the Playwright Locator.

        Args:
            page: Playwright page object.
        """
        if self.locator_fn is not None:
            return self.locator_fn(page)

        if self.selector is not None:
            return page.locator(self.selector)

        raise TypeError("The locator must be defined by either a selector or a callable.")

    def format(self, **kwargs: object) -> PlaywrightLocator:
        """Format a string-based locator.

        Args:
            **kwargs: Named formatting arguments.

        Returns:
            A new locator instance with the formatted name and selector.

        Raises:
            TypeError: If the locator was created using locator_fn.
        """
        if self.selector is None:
            raise TypeError("A locator created with locator_fn cannot be formatted.")

        new_name = self.name.format(**kwargs)
        new_selector = self.selector.format(**kwargs)

        return LocatorPW(
            name=new_name,
            selector=new_selector,
            page=self._page,
        )

    def __getattr__(self, item: str) -> Any:
        """Delegate attribute access to the underlying Locator.

        Args:
            item: Attribute name.

        Returns:
            The requested Locator attribute.

        Raises:
            AttributeError: If the locator is not bound to a page.
        """
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

    def __set_name__(self, owner: type["PagePW"], name: str) -> None:
        """Store the attribute name when the locator is declared on a class.

        Args:
            owner: Class that owns the locator.
            name: Attribute name.
        """
        self._attr_name = name
        self._owner = owner

    def __get__(
        self,
        instance: "PagePW | None",
        owner: type["PagePW"],
    ) -> PlaywrightLocator:
        """Bind the locator to the page object when accessed through an instance.

        Args:
            instance: Page object that owns the locator.
            owner: Class that owns the locator.

        Returns:
            The locator bound to the instance's page.
        """
        if instance is None:
            return self

        page = getattr(instance, "page", None)

        if page is None:
            raise AttributeError(
                f'LocatorPW "{self.name}" requires a "page" attribute on '
                f"{type(instance).__name__}.",
            )

        if self._page is not page:
            self._page = page
            self._cached_locator = None
            self._cached_page = None

        return self

    def __set__(self, instance: "PagePW", value: Never) -> NoReturn:
        """Prevent the locator descriptor from being overwritten on an instance.

        Args:
            instance: Object that owns the descriptor.
            value: Value being assigned.

        Raises:
            AttributeError: Always, because the descriptor is read-only.
        """
        raise AttributeError(
            f'Cannot overwrite LocatorPW "{self._attr_name}". '
            "Use formatting instead: .format(param=value).",
        )


PlaywrightLocator: TypeAlias = LocatorPW | Locator
