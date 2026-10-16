"""Custom soft assertions with logger and Allure steps."""

import linecache
import math
import re
import sys
from collections.abc import Container
from pathlib import Path
from types import FrameType
from typing import Any

from pytest_check import check

from automation.custom.allure_custom.custom_allure import step
from automation.custom.logger.project_logger import logger


def _caller_location() -> tuple[str, str]:
    """Find the first call frame outside this module and pytest_check.

    Returns:
        A tuple of ("path:line (function)", stripped source line).
        Falls back to ("<unknown>", "") if no suitable frame is found.
    """
    frame: FrameType | None = sys._getframe(1)
    while frame is not None:
        module: str = frame.f_globals.get("__name__", "")
        if module != __name__ and not module.startswith("pytest_check"):
            break
        frame = frame.f_back
    if frame is None:
        return "<unknown>", ""

    filename: str = frame.f_code.co_filename
    try:
        path = Path(filename).relative_to(Path.cwd())
    except ValueError:
        path = Path(filename)
    line: str = linecache.getline(filename, frame.f_lineno).strip()
    return f"{path}:{frame.f_lineno} ({frame.f_code.co_name})", line


def _describe(details: str, message: str | None) -> str:
    """Combine a user-provided message with auto-generated details.

    Args:
        details: Auto-generated description (e.g. expected/actual values).
        message: Optional user-provided description.

    Returns:
        "<message>: <details>" if message is given, otherwise details.
    """
    return f"{message}: {details}" if message else details


@check.check_func
def soft_assert(condition: bool, message: str | None = None) -> None:
    """Soft assertion with logger and Allure step.

    The test keeps running after a failure; all failures are reported
    by pytest-check at the end of the test.

    Args:
        condition: The condition that must be true.
        message: Description of the check, used in the Allure step,
            the log and the failure report.

    Raises:
        AssertionError: If the condition is false (collected by pytest-check).

    Examples:
        soft_assert(1 == 1)
        soft_assert(1 == 1, "Values must be equal")
        soft_assert(1 in [1, 2, 3], "1 must be in the list")
    """
    text: str = message or "Condition is not met"
    with step(f"Soft assert: {text}"):
        if not condition:
            location, line = _caller_location()
            log: str = (
                f"Soft assert failed: {text}\n"
                f"{location}\n\tLine: {line}"
            )
            logger.error(log)
            raise AssertionError(log)
        logger.success(f"Soft assert passed: {text}")


def soft_equal(actual: Any, expected: Any, message: str | None = None) -> None:
    """Soft check that two values are equal.

    Args:
        actual: The actual value.
        expected: The expected value.
        message: Optional description of the check.
    """
    details: str = f"expected {expected!r}, got {actual!r}"
    soft_assert(actual == expected, _describe(details, message))


def soft_not_equal(actual: Any, unexpected: Any, message: str | None = None) -> None:
    """Soft check that two values are not equal.

    Args:
        actual: The actual value.
        unexpected: The value that must not match.
        message: Optional description of the check.
    """
    details: str = f"value must not be equal to {unexpected!r}"
    soft_assert(actual != unexpected, _describe(details, message))


def soft_contains(
    container: Container[Any],
    item: Any,
    message: str | None = None,
) -> None:
    """Soft check that an item is present in a container.

    Args:
        container: The collection, string or mapping to search in.
        item: The item that must be present.
        message: Optional description of the check.
    """
    details: str = f"expected {item!r} in {container!r}"
    soft_assert(item in container, _describe(details, message))


def soft_is_close(
    actual: float,
    expected: float,
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
    message: str | None = None,
) -> None:
    """Soft check that two floats are close to each other.

    Args:
        actual: The actual value.
        expected: The expected value.
        rel_tol: Relative tolerance.
        abs_tol: Absolute tolerance (important when comparing values near zero).
        message: Optional description of the check.
    """
    details: str = (
        f"expected {expected!r} (rel_tol={rel_tol}, abs_tol={abs_tol}), "
        f"got {actual!r}"
    )
    soft_assert(
        math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol),
        _describe(details, message),
    )


def soft_matches(text: str, pattern: str, message: str | None = None) -> None:
    """Soft check that a string matches a regular expression (re.search).

    Args:
        text: The string to check.
        pattern: The regular expression pattern.
        message: Optional description of the check.
    """
    details: str = f"expected {text!r} to match {pattern!r}"
    soft_assert(re.search(pattern, text) is not None, _describe(details, message))