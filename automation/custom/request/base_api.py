"""Base class for API groups with optional user authentication."""

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel

from automation.config.settings import get_settings
from automation.config.users import TestUser
from automation.custom.request.request import ApiClient, ClientSettings
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import LoginResponse

R = TypeVar("R", bound=BaseModel)
E = TypeVar("E", bound=BaseModel)


class BaseApi:
    """Base class for API groups with optional user authentication."""

    def __init__(
        self,
        user: TestUser | None = None,
        client: ApiClient | None = None,
        requires_auth: bool = True,
    ) -> None:
        self.requires_auth = requires_auth

        settings = get_settings()

        if client is not None:
            self.client = client
        else:
            client_settings = ClientSettings(base_url=settings.api_base_url)
            self.client = ApiClient(settings=client_settings)

        self.url = self.client.settings.base_url.rstrip("/")

        if user is not None and self.requires_auth:
            self._authenticate(user=user)

    def _authenticate(self, user: TestUser) -> None:
        """Authenticate the user and configure the Bearer token.

        Args:
            user: User to authenticate
        """
        from automation.api.auth import AuthClient

        auth_client = AuthClient(client=self.client)
        response = auth_client.login(
            email=user.email,
            password=user.password.get_secret_value(),
        )
        response.raise_for_status()

        login_data = response.dto()
        if not isinstance(login_data, LoginResponse):
            raise TypeError("Login response was not parsed as LoginResponse")

        self.client.set_auth_token(login_data.access_token)

    def request(
        self,
        url: str,
        method: str = "GET",
        headers: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | BaseModel | None = None,
        json: Mapping[str, Any] | BaseModel | list[Any] | None = None,
        data: Mapping[str, Any] | list[Any] | str | bytes | BaseModel | None = None,
        response_model: type[R] | None = None,
        response_error_model: type[E] | None = None,
        **kwargs: Any,
    ) -> CustomResponse[R, E]:
        return self.client.request(
            path=url,
            method=method,
            headers=headers,
            params=params,
            json=json,
            data=data,
            response_model=response_model,
            response_error_model=response_error_model,
            **kwargs,
        )