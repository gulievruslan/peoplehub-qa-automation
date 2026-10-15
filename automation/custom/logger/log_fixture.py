from collections.abc import Callable, Generator
from functools import wraps
from inspect import isgeneratorfunction
from typing import Any, TypeVar, cast

from automation.custom.logger.project_logger import logger

F = TypeVar("F", bound=Callable[..., Any])


def log_fixture(func: F) -> F:
    """Log fixture setup, teardown, and failures."""
    fixture_name = func.__name__

    if isgeneratorfunction(func):

        @wraps(func)
        def generator_wrapper(*args: Any, **kwargs: Any) -> Generator[Any, Any, None]:
            logger.info(f"Setting up fixture: {fixture_name}")

            try:
                yield from func(*args, **kwargs)
            except Exception:
                logger.exception(f"Fixture failed: {fixture_name}")
                raise
            finally:
                logger.info(f"Fixture teardown finished: {fixture_name}")

        return cast(F, generator_wrapper)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Setting up fixture: {fixture_name}")

        try:
            result = func(*args, **kwargs)
            logger.success(f"Fixture setup completed: {fixture_name}")
            return result
        except Exception:
            logger.exception(f"Fixture setup failed: {fixture_name}")
            raise

    return cast(F, wrapper)