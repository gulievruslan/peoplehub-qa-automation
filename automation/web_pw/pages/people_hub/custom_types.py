"""Custom data types and selector builders for PeopleHub Page Objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias


@dataclass(frozen=True)
class Button:
    """Describe a button by its accessible name and optional test ID.

    Attributes:
        name: Accessible name or visible label of the button.
        data_testid: Optional value of the data-testid attribute.
    """

    name: str
    data_testid: str | None = None

    def __post_init__(self) -> None:
        """Validate the button description."""

        if not self.name.strip():
            raise ValueError("Button name must not be empty.")

        if self.data_testid is not None and not self.data_testid.strip():
            raise ValueError("Button data_testid must not be empty when provided.")


SelectorType = Literal["testid", "text", "css"]


@dataclass(frozen=True)
class SelectorStep:
    """Represent one step in a locator chain.

    Attributes:
        by: Locator strategy: testid, text, or css.
        value: Value used by the selected locator strategy.
        nth: Optional zero-based index of the matching element.
    """

    by: SelectorType
    value: str
    nth: int | None = None

    def __post_init__(self) -> None:
        """Validate the selector step."""

        if not self.value.strip():
            raise ValueError("Selector value must not be empty.")

        if self.nth is not None and self.nth < 0:
            raise ValueError("Selector index must be zero or greater.")

    def __repr__(self) -> str:
        """Return a compact representation suitable for logs."""

        base = f'{self.by}="{self.value}"'

        if self.nth is not None:
            base += f"[{self.nth}]"

        return base


@dataclass(frozen=True)
class NestedSelector:
    """Represent a child selector resolved within a parent selector."""

    parent: SelectorChain
    child: SelectorChain


SelectorChain: TypeAlias = SelectorStep | NestedSelector


def by_test_id(test_id: str) -> SelectorStep:
    """Create a selector step using a data-testid attribute.

    Args:
        test_id: Value of the data-testid attribute.
    """

    return SelectorStep(by="testid", value=test_id)


def by_text(text: str) -> SelectorStep:
    """Create a selector step using text content.

    Args:
        text: Text to search for.
    """

    return SelectorStep(by="text", value=text)


def by_css(selector: str) -> SelectorStep:
    """Create a selector step using a CSS selector.

    Args:
        selector: CSS selector used to locate the element.
    """

    return SelectorStep(by="css", value=selector)


def at_nth(selector: SelectorStep, index: int) -> SelectorStep:
    """Return a copy of a selector step targeting a zero-based index.

    Args:
        selector: Original selector step.
        index: Zero-based index of the matching element.

    Raises:
        ValueError: If the index is negative.
    """

    return SelectorStep(by=selector.by, value=selector.value, nth=index)


def inside(parent: SelectorChain, child: SelectorChain) -> NestedSelector:
    """Describe a child selector that must be resolved inside a parent selector.

    Args:
        parent: Selector identifying the parent element or container.
        child: Selector identifying an element within the parent.
    """

    return NestedSelector(parent=parent, child=child)