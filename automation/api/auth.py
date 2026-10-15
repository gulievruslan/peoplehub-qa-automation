"""API client for PeopleHub authentication endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import (
    InvalidCredentialsResponse,
    LoginResponse,
    UserResponse,
)


class AuthClient(Base):
    """API client for PeopleHub authentication endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the authentication API client.

        Args:
            **kwargs: Additional keyword arguments passed to the API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/auth"

    def login(
        self,
        email: str,
        password: str | None = None,
    ) -> CustomResponse[LoginResponse, InvalidCredentialsResponse]:
        """Authenticate a user and return the login response.

        Args:
            email: The email address of the user to authenticate.
            password: The password of the user to authenticate.
        """
        return self.request(
            method="POST",
            url=f"{self.url}/login",
            json={"email": email, "password": password},
            response_model=LoginResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_me(
        self, access_token: str | None = None,
    ) -> CustomResponse[UserResponse, InvalidCredentialsResponse]:
        """Get the currently authenticated user.

        Args:
            access_token (str): The access token to retrieve the current user.
        """
        headers = (
            {"Authorization": f"Bearer {access_token}"} if access_token is not None else None
        )

        return self.request(
            method="GET",
            url=f"{self.url}/me",
            headers=headers,
            response_model=UserResponse,
            response_error_model=InvalidCredentialsResponse,
        )