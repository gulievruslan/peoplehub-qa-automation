"""Декоратор для создания скриншотов методов Page Object."""
from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

import allure


DecFunc = TypeVar("DecFunc", bound=Callable[..., Any])


def make_screenshot(decorated: DecFunc) -> DecFunc:
    """Декоратор для создания скриншота методов Page Object.

    Args:
        decorated: декорируемый метод.

    Returns:
        Обёрнутый метод.
    """

    @functools.wraps(decorated)
    def inner(*args: Any, **kwargs: Any) -> Any:
        """Обёртка над методами Page Object."""
        self_obj = args[0] if args else kwargs.get("self")
        page = getattr(self_obj, "page", None) if self_obj else None
        exception: Exception | None = None
        result: Any = None

        try:
            result = decorated(*args, **kwargs)

        except Exception as e:
            exception = e

        if page is not None:
            try:
                label = "success" if exception is None else "error"
                allure.attach(
                    body=page.screenshot(full_page=True),
                    name=f"Скриншот: {decorated.__name__} — {label}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass

        if exception:
            raise exception

        return result  # type: ignore[return-value]

    return inner
