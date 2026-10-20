"""Module containing a custom response wrapper."""

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Self, cast, overload

from allure import step
from pydantic import BaseModel
from requests import Response
from requests.cookies import RequestsCookieJar
from requests.structures import CaseInsensitiveDict
from requests.utils import dict_from_cookiejar

from automation.custom.logger.project_logger import logger
from automation.custom.validation.is_valid import is_valid
from automation.custom.validation.is_value_json import is_value_json

ERROR_SUCCESS_MSG = 'The "success" field does not match the expected value: {result}'
ERROR_STATUS_CUSTOM_MSG = "Response status code {code} does not match the expected code: {exp}"

_UNSET = object()


class CustomResponse[R: BaseModel, E: BaseModel | None]:
    """Extend the standard Response with model validation support."""

    __slots__ = [
        "response",
        "response_model",
        "response_error_model",
        "_response_body",
        "_dto",
        "_neg_dto",
    ]

    def __init__(
        self,
        response: Response,
        response_model: type[R] | None = None,
        response_error_model: type[E] | None = None,
    ):
        """Initialize the response wrapper.

        Args:
            response: The response returned by an HTTP request.
            response_model: The model used to validate a successful response.
            response_error_model: The model used to validate an error response.
        """
        self.response = response
        self._response_body: Any = _UNSET
        self.response_model = response_model
        self.response_error_model = response_error_model
        self._dto: R | None = None
        self._neg_dto: E | None = None

    @property
    def status_code(self) -> int:
        """Return the HTTP status code."""
        logger.debug("Accessing status_code from the Response object")
        return self.response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        """Return the response headers."""
        logger.debug("Accessing headers from the Response object")
        return self.response.headers

    @property
    def content(self) -> bytes:
        """Return the response body as bytes."""
        logger.debug("Accessing content from the Response object")
        return self.response.content

    @property
    def text(self) -> str:
        """Return the response body as a string."""
        logger.debug("Accessing text from the Response object")
        return self.response.text

    @property
    def history(self) -> list[Response]:
        """Return the response history."""
        logger.debug("Accessing history from the Response object")
        return self.response.history

    @property
    def links(self) -> dict[str, Any]:
        """Return the response links as a dictionary."""
        logger.debug("Accessing links from the Response object")
        return self.response.links

    @property
    def cookies(self) -> RequestsCookieJar:
        """Return the response cookies."""
        logger.debug("Accessing cookies from the Response object")
        return self.response.cookies

    @property
    def cookies_as_dict(self) -> dict[str, Any]:
        """Return the response cookies as a dictionary."""
        result = dict_from_cookiejar(self.cookies)
        logger.success("Converted response cookies to a dictionary: {}", result)
        return result

    @step("Raise an exception for an unsuccessful status code")
    def raise_for_status(self) -> Self:
        """Raise HTTPError if the response status indicates a client or server error."""
        logger.debug("Calling raise_for_status on the Response object")
        self.response.raise_for_status()
        return self

    @step("Parse the response body as a dictionary or list")
    def json(self, **kwargs: Any) -> Any:
        """Return the parsed JSON response body.

        Args:
            **kwargs: Additional arguments passed to Response.json().
        """
        logger.debug("Parsing the response body as a Python object")

        if self._response_body is _UNSET:
            logger.debug("Response body is not cached. Parsing the Response object")
            self._response_body = self.response.json(**kwargs)
            logger.debug("Parsed response body and cached it")
        else:
            logger.debug("Returning the cached response body")

        return self._response_body

    @step("Get the success field")
    def success(self) -> Any:
        """Return the value of the success field, if present."""
        body = self.json()

        if isinstance(body, dict):
            result = body.get("success")
            logger.debug("Retrieved the success field: {}", result)
            return result

        logger.warning(
            "The response body is not a dictionary. Cannot retrieve the success field. "
            "Response body type: {}",
            type(body).__name__,
        )
        return None

    @overload
    def dto(self, is_error_model: Literal[False] = False, context: dict[str, Any] | None = None) -> R: ...

    @overload
    def dto(self, is_error_model: Literal[True] = True, context: dict[str, Any] | None = None) -> E: ...

    @step("Convert the response to a DTO")
    def dto(self, is_error_model: bool = False, context: dict[str, Any] | None = None) -> R | E:
        """Convert the response body to a data transfer object.

        Args:
            is_error_model: Whether to use the error response model.
            context: Additional context passed to Pydantic validation.
        """
        model_ = self.response_error_model if is_error_model else self.response_model
        dto = self._neg_dto if is_error_model else self._dto

        if model_ is None:
            model_type = "Error " if is_error_model else ""
            raise AttributeError(f"{model_type}response model is not configured")

        if dto is not None:
            logger.info("DTO is already cached. Returning the cached DTO")
            return dto

        if not issubclass(model_, BaseModel):
            raise AttributeError(
                f"Invalid model {model_!r}: it does not inherit from BaseModel. "
                f"Model type: {type(model_).__name__}"
            )

        result = model_.model_validate(self.json(), context=context)
        logger.debug("Successfully converted the response body to a DTO: {}", result)

        if is_error_model:
            self._neg_dto = result  # type: ignore[assignment]
        else:
            self._dto = result  # type: ignore[assignment]

        return result

    def __get_http_exchange_details(self) -> str:
        """Return HTTP request and response details for debugging."""
        request = self.response.request
        response = self.response

        sensitive_headers = {
            "authorization",
            "cookie",
            "set-cookie",
            "proxy-authorization",
        }

        def format_headers(headers: Mapping[str, str | bytes]) -> str:
            return "\n".join(
                f"{key}: {'***REDACTED***' if key.lower() in sensitive_headers else value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value}"
                for key, value in headers.items()
            ) or "<empty>"

        request_body = request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode("utf-8", errors="replace")

        response_body = response.text

        return (
            "\n\n========== HTTP REQUEST ==========\n"
            f"{request.method} {request.url}\n"
            f"Headers:\n{format_headers(request.headers)}\n"
            f"Body:\n{request_body if request_body is not None else '<empty>'}\n"
            "\n========== HTTP RESPONSE ==========\n"
            f"Status: {response.status_code}\n"
            f"Headers:\n{format_headers(response.headers)}\n"
            f"Body:\n{response_body if response_body else '<empty>'}\n"
            "=================================="
        )

    @step("Check the response status code")
    def __base_check_expected_status_code(
        self,
        expected_code: int | Sequence[int],
        exception: type[Exception] | None = None,
        message: str | None = None,
        **kwargs: Any,
    ):
        """Check whether the response status code matches the expected value.

        Args:
            expected_code: An expected status code or a sequence of accepted codes.
            exception: Exception class to raise instead of using an assertion.
            message: Additional text appended to the default error message.
            **kwargs: Additional keyword arguments passed to the exception.
        """
        msg = ERROR_STATUS_CUSTOM_MSG.format(
            code=self.status_code,
            exp=expected_code,
        )

        if message:
            msg = f"{msg}. {message}"

        expected_codes = (expected_code,) if isinstance(expected_code, int) else tuple(expected_code)

        if self.status_code not in expected_codes:
            details = self.__get_http_exchange_details()
            logger.error("HTTP exchange failed validation: {}", details)

            if exception is not None:
                logger.debug("Checking the response status code using an exception")
                raise exception(f"{msg}. Full HTTP exchange logged above.", **kwargs)

            logger.debug("Checking the response status code using an assertion")
            assert self.status_code in expected_codes, f"{msg}{details}"

        logger.success("Response status code validated successfully")

    @step("Assert the response status code")
    def assert_status_code(
        self,
        expected_code: int | Sequence[int] = 200,
        message: str | None = None,
    ) -> Self:
        """Assert that the response status code is expected.

        Args:
            expected_code: An expected status code or a sequence of accepted codes.
            message: Additional text appended to the default error message.
        """
        self.__base_check_expected_status_code(
            expected_code=expected_code,
            message=message,
        )
        return self

    @step("Check the response status code and raise an exception on failure")
    def check_status_code(
        self,
        expected_code: int | Sequence[int] = 200,
        exception: type[Exception] = ValueError,
        message: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Check the response status code and raise an exception on failure.

        Args:
            expected_code: An expected status code or a sequence of accepted codes.
            exception: Exception class to raise when validation fails.
            message: Additional text appended to the default error message.
            **kwargs: Additional keyword arguments passed to the exception.
        """
        self.__base_check_expected_status_code(
            expected_code=expected_code,
            exception=exception,
            message=message,
            **kwargs,
        )
        return self

    def __base_is_success(
        self,
        exception: type[Exception] | None = None,
        reverse: bool = False,
        message: str | None = None,
        **kwargs: Any,
    ):
        """Check the success field in the response.

        Args:
            exception: Exception class to raise instead of using an assertion.
            reverse: Whether to expect success to be False.
            message: Additional text appended to the default error message.
            **kwargs: Additional keyword arguments passed to the exception.
        """
        success = self.success()
        msg = ERROR_SUCCESS_MSG.format(result="false" if reverse else "true")

        if message:
            msg = f"{msg}. {message}"

        if not isinstance(success, bool):
            raise ValueError(
                f"Expected a boolean value for the success field. Actual value: {success!r}"
            )

        logger.debug(
            "Validating the success field: {}",
            "expecting False" if reverse else "expecting True",
        )

        result = not success if reverse else success

        if exception is not None:
            logger.debug("Checking the success field using an exception")

            if not result:
                raise exception(msg, **kwargs)
        else:
            logger.debug("Checking the success field using an assertion")
            assert result, msg

        logger.success("Success field validated successfully")

    @step("Assert the success field")
    def assert_is_success(self, reverse: bool = False, message: str | None = None) -> Self:
        """Assert that the success field has the expected boolean value."""
        self.__base_is_success(reverse=reverse, message=message)
        return self

    @step("Check the success field and raise an exception on failure")
    def check_is_success(
        self,
        exception: type[Exception] = ValueError,
        reverse: bool = False,
        message: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Check the success field and raise an exception on failure."""
        self.__base_is_success(
            exception=exception,
            reverse=reverse,
            message=message,
            **kwargs,
        )
        return self

    @step("Validate the response body against the expected model")
    def assert_model_valid[Model: BaseModel](
        self,
        expected_model: type[Model] | type[int] | type[str] | type[bool] | None = None,
        is_error_model: bool = False,
        context: dict[str, Any] | None = None,
    ) -> Self:
        """Validate the response body against the expected model.

        Args:
            expected_model: Optional Pydantic model or primitive type used for validation.
            is_error_model: Whether to use the configured error response model.
            context: Additional context passed to Pydantic validation.
        """
        model_: type[Model] | type[R] | type[E] | type[int] | type[str] | type[bool] | None = expected_model

        if model_ is None:
            model_ = self.response_error_model if is_error_model else self.response_model

        assert model_ is not None, "No response model configured."

        response_body = self.json()

        if isinstance(model_, type) and issubclass(model_, BaseModel):
            is_valid(
                model=cast(type[BaseModel], model_),
                response=response_body,
                context=context,
            )
        else:
            assert isinstance(response_body, model_), (
                f"Expected response body of type {model_.__name__}, "
                f"got {type(response_body).__name__}"
            )

        logger.success("Response body validated successfully")
        return self

    @step("Check whether the response body contains valid JSON")
    def is_body_json(self, **kwargs: Any) -> bool:
        """Check whether the response body contains valid JSON.

        Args:
            **kwargs: Additional arguments passed to the JSON validation helper.
        """
        logger.debug("Checking whether the response body contains valid JSON")
        return is_value_json(value=self.content, **kwargs)
