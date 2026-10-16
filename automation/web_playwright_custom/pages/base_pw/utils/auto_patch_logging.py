"""Utilities for logging public callable attributes of an object."""

from collections.abc import Callable
from functools import wraps
from typing import Any, cast

from automation.custom.logger.project_logger import logger


def _create_wrapper[**P, RET](
    method: Callable[P, RET],
    name: str,
    log_prefix: str,
    log_return: bool,
) -> Callable[P, RET]:
    """Create a wrapper that logs method calls, return values, and exceptions."""

    @wraps(method)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> RET:
        logger.debug(f"{log_prefix}.{name}()")

        try:
            result = method(*args, **kwargs)

            if log_return:
                logger.debug(f"{log_prefix}.{name} completed")

            return result
        except Exception:
            logger.exception(f"{log_prefix}.{name} raised an exception")
            raise

    cast(Any, wrapper)._auto_patch_logging_wrapper = True
    return wrapper


def _auto_patch_logging(
    obj: object,
    log_prefix: str,
    log_return: bool = False,
) -> None:
    """Add logging to all public callable attributes of an object."""

    for attr_name in (name for name in dir(obj) if not name.startswith("_")):
        original: Any = getattr(obj, attr_name)

        if callable(original) and not getattr(original, "_auto_patch_logging_wrapper", False):
            setattr(
                obj,
                attr_name,
                _create_wrapper(
                    method=original,
                    name=attr_name,
                    log_prefix=log_prefix,
                    log_return=log_return,
                ),
            )
