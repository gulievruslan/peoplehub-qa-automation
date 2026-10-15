"""Base DTO for PeopleHub API automation."""

from typing import Any

from automation.custom.request.base_api import BaseApi


class Base(BaseApi):
    """Base API client for PeopleHub endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the base API client."""
        super().__init__(**kwargs)
        self.url = f"{self.url}/api"
