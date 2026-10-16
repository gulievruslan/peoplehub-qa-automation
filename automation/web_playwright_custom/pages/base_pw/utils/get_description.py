"""Utility for generating human-readable object descriptions."""

from playwright.sync_api import APIResponse, Locator, Page

from automation.web_playwright_custom.pages.base_pw.locators.locators import LocatorPW


def get_description(
    target: Locator | LocatorPW | Page | APIResponse,
    description: str | None = None,
) -> str:
    """Generate a human-readable description of an object.

    Args:
        target: Object being checked.
        description: Optional custom description.

    Returns:
        A human-readable description of the target.
    """

    if description is not None:
        return description

    if isinstance(target, LocatorPW):
        return str(target)

    if isinstance(target, Page):
        return f"Page(url='{target.url}')"

    if isinstance(target, APIResponse):
        return f"APIResponse(url='{target.url}', status={target.status})"

    if isinstance(target, Locator):
        return target.description or f"Locator@{id(target):x}"

    return f"{type(target).__name__}@{id(target):x}"