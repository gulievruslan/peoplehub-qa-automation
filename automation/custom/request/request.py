"""HTTP client for a backend service running in Docker."""

import os
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from http.cookiejar import CookieJar
from types import TracebackType
from typing import Any, Self, TypeVar

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from automation.custom.logger import log_response, log_request
from automation.custom.logger.project_logger import logger
from automation.custom.model.model import convert_models_to_request
from automation.custom.response.custom_response import CustomResponse

R = TypeVar("R", bound=BaseModel)
E = TypeVar("E", bound=BaseModel)


class BackendUnavailableError(ConnectionError):
    """Raised when the backend container cannot be reached."""


@dataclass(frozen=True)
class ClientSettings:
    """Connection settings for the API client.

    Attributes:
        base_url: Root URL of the backend (host port or compose service name).
        timeout: Default response timeout in seconds.
        verify: Whether to verify TLS certificates.
        connect_retries: Number of retries for failed connections only.
        trust_env: Whether to use proxy variables from the environment.
    """

    base_url: str = field(default_factory=lambda: os.getenv("API_BASE_URL", "http://localhost:8080"))
    timeout: float = field(default_factory=lambda: float(os.getenv("API_TIMEOUT", "10")))
    verify: bool = True
    connect_retries: int = 3
    trust_env: bool = False


class ApiClient:
    """Send API requests to a backend running in Docker."""

    def __init__(
        self,
        settings: ClientSettings | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Initialize the client and open a session.

        Args:
            settings: Connection settings. Defaults are read from environment variables.
            headers: Default headers sent with every request.
        """
        self.settings: ClientSettings = settings or ClientSettings()
        self.headers: dict[str, str] = dict(headers or {})
        self.session: requests.Session = self._build_session()

    def _build_session(self) -> requests.Session:
        """Create a session that retries only failed connections.

        Returns:
            A configured requests session.
        """
        session = requests.Session()
        session.trust_env = self.settings.trust_env
        retry = Retry(
            total=None,
            connect=self.settings.connect_retries,
            read=0,
            status=0,
            backoff_factor=0.5,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _build_url(self, path: str) -> str:
        """Build an absolute URL from a path.

        Args:
            path: Endpoint path (e.g. "/users/1") or an absolute URL.

        Returns:
            The absolute URL.
        """
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.settings.base_url.rstrip('/')}/{path.lstrip('/')}"

    def __enter__(self) -> Self:
        """Return the client for use in a with block."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Close the session when leaving the with block.

        Args:
            exc_type: Exception class raised inside the block, if any.
            exc_val: Exception instance raised inside the block, if any.
            exc_tb: Traceback of the exception, if any.
        """
        self.close()

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()

    def set_auth_token(self, token: str) -> None:
        """Set the Bearer token for subsequent requests."""
        self.headers["Authorization"] = f"Bearer {token}"

    def wait_until_ready(
        self,
        path: str = "/health",
        timeout: float = 60.0,
        interval: float = 1.0,
    ) -> None:
        """Wait until the backend answers a health endpoint with a 2xx status.

        Args:
            path: Health check endpoint path.
            timeout: Maximum time to wait in seconds.
            interval: Pause between attempts in seconds.

        Raises:
            BackendUnavailableError: If the backend is not ready in time.
        """
        deadline = time.monotonic() + timeout
        last_error = "no attempts made"

        while time.monotonic() < deadline:
            try:
                response = self.session.get(
                    url=self._build_url(path=path),
                    timeout=self.settings.timeout,
                    verify=self.settings.verify,
                )
                if response.ok:
                    logger.success("Backend is ready: {}", self._build_url(path=path))
                    return
                last_error = f"status code {response.status_code}"
            except requests.RequestException as error:
                last_error = repr(error)

            time.sleep(interval)

        raise BackendUnavailableError(
            f"Backend is not ready after {timeout}s at {self.settings.base_url}. "
            f"Last error: {last_error}"
        )

    def request(
        self,
        path: str,
        method: str = "GET",
        headers: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | BaseModel | None = None,
        data: Mapping[str, Any] | list | str | bytes | BaseModel | None = None,
        json: Mapping[str, Any] | BaseModel | list | None = None,
        files: Mapping[str, Any] | list | None = None,
        cookies: Mapping[str, Any] | CookieJar | None = None,
        timeout: float | None = None,
        allow_redirects: bool = True,
        needs_allure: bool = True,
        needs_log: bool = True,
        response_model: type[R] | None = None,
        response_error_model: type[E] | None = None,
        **kwargs: Any,
    ) -> CustomResponse[R, E]:
        """Send a request, log it and wrap the response.

        Args:
            path: Endpoint path or an absolute URL.
            method: HTTP method.
            headers: Extra headers merged over the client's default headers.
            params: Query parameters.
            data: Request body (form data, string or bytes).
            json: Request body serialized as JSON.
            files: Files to upload.
            cookies: Cookies to send.
            timeout: Response timeout in seconds. Defaults to the client setting.
            allow_redirects: Whether to follow redirects.
            needs_allure: Whether to attach the request and response to Allure.
            needs_log: Whether to log the request.
            response_model: Model for a successful response.
            response_error_model: Model for an error response.
            **kwargs: Extra arguments for the model conversion helper.

        Returns:
            The response wrapped in CustomResponse.

        Raises:
            BackendUnavailableError: If the backend cannot be reached.
        """
        url = self._build_url(path=path)

        json_body, data_body, query = convert_models_to_request(
            json=json,
            data=data,
            params=params,
            **kwargs,
        )

        prepared = self.session.prepare_request(
            requests.Request(
                method=method,
                url=url,
                headers={**self.headers, **(headers or {})},
                params=query,
                data=data_body,
                json=json_body,
                files=files,
                cookies=cookies,
            )
        )

        if needs_log:
            log_request(
                request=prepared,
                is_insecure=not self.settings.verify,
                needs_allure=needs_allure,
            )

        try:
            response = self.session.send(
                request=prepared,
                timeout=timeout if timeout is not None else self.settings.timeout,
                verify=self.settings.verify,
                allow_redirects=allow_redirects,
            )
        except requests.ConnectionError as error:
            raise BackendUnavailableError(
                f"Backend is not reachable at {self.settings.base_url}. "
                "Check that the container is up and the port is published."
            ) from error

        log_response(response=response, needs_allure=needs_allure)

        return CustomResponse(
            response=response,
            response_model=response_model,
            response_error_model=response_error_model,
        )