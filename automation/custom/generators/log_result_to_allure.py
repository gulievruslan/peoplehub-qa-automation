from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from allure import attach, attachment_type, step

from automation.custom.logger.project_logger import logger

Result = str | dict[Any, Any] | list[Any] | bool | int
Decorated = TypeVar("Decorated", bound=Callable[..., Result])


def log_result_to_allure(name: str) -> Callable[[Decorated], Decorated]:
    """Decorate a function that retrieves a token.

    Args:
        name: The generator name.
    """

    def wrapper(decorated: Decorated) -> Decorated:
        @wraps(decorated)
        def inner(**kwargs: Any) -> Result:
            """Run the generator and attach its result to Allure."""
            needs_allure = kwargs.get("needs_allure", True)

            logger.info(f'Running generator "{name}"')
            result = decorated(**kwargs)
            logger.success(f"Generator completed successfully!\n\tResult: {result}")

            if needs_allure:
                try:
                    with step(name):
                        attach(body=str(result), name="RESULT", attachment_type=attachment_type.TEXT)
                except KeyError:
                    logger.warning(
                        "The test session has not been created yet! "
                        "Cannot attach the generator result to Allure!"
                    )

            return result

        return cast(Decorated, inner)

    return wrapper
