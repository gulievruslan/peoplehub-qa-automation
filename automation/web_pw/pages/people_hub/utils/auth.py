"""Authentication helpers for PeopleHub UI tests."""
import requests

from automation.config.settings import get_settings
from automation.config.users import TestUser


def get_access_token(user: TestUser) -> str:
    """Authenticate a test user through the API and return the access token.

    Args:
        user: Test user whose credentials are used for authentication.

    Returns:
        JWT access token.

    Raises:
        requests.HTTPError: If the authentication request fails.
        requests.RequestException: If the request cannot be completed.
        KeyError: If the response does not contain an access token.
        TypeError: If the access token is not a string.
    """
    settings = get_settings()
    response = requests.post(
        url=f"{settings.api_base_url.rstrip('/')}/api/auth/login",
        json={"email": user.email, "password": user.password.get_secret_value()},
        timeout=15,
    )
    response.raise_for_status()

    access_token = response.json()["access_token"]

    if not isinstance(access_token, str):
        raise TypeError("Expected access_token to be a string")

    return access_token