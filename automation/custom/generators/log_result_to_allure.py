from typing import Callable

from allure import attach, attachment_type, step

from automation.custom.logger.project_logger import logger


def log_result_to_allure(name: str) -> Callable:
    """Decorate a function that retrieves a token.

    Args:
        name: The generator name.
    """

    def wrapper(decorated: Callable):
        def inner(**kwargs) -> str | dict | list | bool | int:
            """Wrapper around the generator.

            Args:
                **kwargs: Additional keyword arguments.
            """
            if needs_allure := kwargs.get('needs_allure', True):
                (allure_step := step(name)).__enter__()

            logger.info(f'Running generator "{name}"')
            result = decorated(**kwargs)
            logger.success(f'Generator completed successfully!\n\tResult: {result}')

            if needs_allure:
                try:
                    attach(body=str(result), name='RESULT', attachment_type=attachment_type.TEXT)
                    allure_step.__exit__(exc_type=None, exc_val=None, exc_tb=None)

                except KeyError:
                    logger.warning(
                        'The test session has not been created yet! '
                        'Cannot attach the generator result to Allure!'
                    )

            return result

        return inner

    return wrapper