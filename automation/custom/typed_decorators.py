"""Typed wrappers for third-party test decorators."""

from collections.abc import Callable
from typing import Any, TypeVar, cast

from allure import label, title
from qase.pytest import qase

F = TypeVar("F", bound=Callable[..., Any])


def typed_title(value: str) -> Callable[[F], F]:
    """Apply an Allure title without losing the decorated callable's type.

    Args:
        value: Title to display in the Allure report.

    Returns:
        A decorator that preserves the decorated callable's type.
    """
    return cast(Callable[[F], F], title(value))


def typed_qase_id(qase_id: int | list[int]) -> Callable[[F], F]:
    """Apply Qase IDs and add them to Allure results.

    Args:
        qase_id: A single Qase test case ID or a list of test case IDs.

    Returns:
        A decorator that preserves the decorated callable's type.
    """
    case_ids = qase_id if isinstance(qase_id, list) else [qase_id]

    def decorator(func: F) -> F:
        decorated = func

        for case_id in case_ids:
            decorated = cast(F, label("qase_id", str(case_id))(decorated))

        return cast(F, qase.id(id=qase_id)(decorated))

    return decorator
