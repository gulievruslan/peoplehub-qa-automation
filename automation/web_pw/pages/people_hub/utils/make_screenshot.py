"""Decorator for taking screenshots of Page Object methods."""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, cast

import allure
from playwright.sync_api import Page


def make_screenshot[DecFunc: Callable[..., Any]](decorated: DecFunc) -> DecFunc:
    """Take a screenshot after a Page Object method executes."""

    @functools.wraps(decorated)
    def inner(*args: Any, **kwargs: Any) -> Any:
        """Execute the method and attach a screenshot to the Allure report."""
        self_obj = args[0] if args else kwargs.get("self")
        page = getattr(self_obj, "page", None) if self_obj else None
        exception: Exception | None = None

        try:
            result = decorated(*args, **kwargs)
        except Exception as error:
            exception = error
            result = None

        if isinstance(page, Page) and exception is not None:
            try:
                allure.attach(
                    body=page.screenshot(full_page=True),
                    name=f"Screenshot: {decorated.__name__} — error",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass

        if exception is not None:
            raise exception

        return result

    return cast(DecFunc, inner)