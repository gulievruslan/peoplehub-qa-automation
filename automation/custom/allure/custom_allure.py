"""Custom Allure steps with console logger."""

from collections.abc import Callable
from functools import wraps
from typing import Any, cast

import allure

from automation.custom.logger.project_logger import logger


def step(title: str, log_level: str = "INFO") -> Any:
    """Create an Allure step supporting decorators and context managers."""

    log_method = cast(
        Callable[[str], Any],
        getattr(logger, log_level.lower(), logger.info),
    )

    class StepContext:
        """Context manager for logged Allure steps."""

        def __enter__(self) -> Any:
            log_method(title)
            self.context = allure.step(title)
            return self.context.__enter__()

        def __exit__(self, *args: Any) -> Any:
            return self.context.__exit__(*args)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with StepContext():
                return func(*args, **kwargs)

        return wrapper

    class StepFactory:
        """Support both decorator and context manager usage."""

        def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
            return decorator(func)

        def __enter__(self) -> Any:
            self.context = StepContext()
            return self.context.__enter__()

        def __exit__(self, *args: Any) -> Any:
            return self.context.__exit__(*args)

    return StepFactory()
