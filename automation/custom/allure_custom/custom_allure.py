
"""Custom Allure steps with console logger."""

from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

import allure

from automation.custom.logger.project_logger import logger

P = ParamSpec("P")
R = TypeVar("R")


class StepContext:
    """Context manager for logged Allure steps."""

    def __init__(self, title: str, log_method: Callable[[str], Any]) -> None:
        self.title = title
        self.log_method = log_method
        self.context: Any = None

    def __enter__(self) -> Any:
        self.log_method(self.title)
        self.context = allure.step(self.title)
        return self.context.__enter__()

    def __exit__(self, *args: Any) -> Any:
        return self.context.__exit__(*args)


class StepFactory:
    """Support both decorator and context manager usage."""

    def __init__(self, title: str, log_method: Callable[[str], Any]) -> None:
        self.title = title
        self.log_method = log_method

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a function with an Allure step."""
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                step_title = self.title.format(**kwargs)
            except (KeyError, IndexError, ValueError):
                step_title = self.title

            with StepContext(step_title, self.log_method):
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self) -> Any:
        self.context = StepContext(self.title, self.log_method)
        return self.context.__enter__()

    def __exit__(self, *args: Any) -> Any:
        return self.context.__exit__(*args)


def step(title: str, log_level: str = "INFO") -> StepFactory:
    """Create an Allure step supporting decorators and context managers."""
    log_method = cast(
        Callable[[str], Any],
        getattr(logger, log_level.lower(), logger.info),
    )
    return StepFactory(title, log_method)
