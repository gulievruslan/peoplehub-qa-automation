
"""Pydantic validation helpers for API responses."""

from json import dumps
from typing import Any

import allure
import pytest
from loguru import logger
from pydantic import BaseModel, TypeAdapter, ValidationError


class ModelValidateOtherError(Exception):
    """Raised when response validation cannot be performed."""


@logger.catch
@allure.step("Validate response body against schema")
def is_valid(
    model: type[BaseModel],
    response: dict | list | int | str | bool,
    context: dict[str, Any] | None = None,
):
    """Validate a response body against a Pydantic model.

    Args:
        model: Pydantic model used to validate the response.
        response: Parsed JSON response body.
        context: Optional context passed to Pydantic validators.
    """
    with allure.step("Validate response body"):
        model_json = None
        response_json = None

        try:
            if not isinstance(model, type) or not issubclass(model, BaseModel):
                raise ModelValidateOtherError(
                    "The validation schema must inherit from BaseModel."
                )

            model_json = dumps(model.model_json_schema(), ensure_ascii=False, indent=2)
            response_json = dumps(response, ensure_ascii=False, indent=2)

            allure.attach(
                response_json,
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                model_json,
                name="Validation schema",
                attachment_type=allure.attachment_type.JSON,
            )

            if isinstance(response, list) and not model.__pydantic_root_model__:
                logger.warning(
                    "Validating a list response with a non-root model. "
                    "Pass a RootModel or a model representing the expected response."
                )
                TypeAdapter(list[model]).validate_python(response, context=context)
            else:
                model.model_validate(response, context=context)

        except ValidationError as error:
            logger.error(
                "Response body validation failed.\n"
                f"Error:\n{error}\n"
                f"Model:\n{model_json or model}\n"
                f"Response:\n{response_json or response}"
            )
            pytest.fail(str(error), pytrace=False)

        except ModelValidateOtherError:
            raise

        except (TypeError, AttributeError, ValueError) as error:
            raise ModelValidateOtherError(
                "An error occurred during response validation.\n"
                f"Model: {model!r} (type: {type(model).__name__})\n"
                f"Response type: {type(response).__name__}\n"
                f"Details: {error}"
            ) from error
