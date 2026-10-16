"""Utility for extracting a Playwright Page instance from decorated method arguments."""

from playwright.sync_api import Page


def _extract_page_from_args(args: tuple[object, ...]) -> Page | None:
    """Extract a Playwright Page instance from the first argument, if available.

    Args:
        args: Positional arguments passed to the decorated function or method.

    Returns:
        The Playwright Page instance, or None if it cannot be extracted.
    """

    if not args:
        return None

    self_or_cls = args[0]
    page = getattr(self_or_cls, "page", None)

    return page if isinstance(page, Page) else None