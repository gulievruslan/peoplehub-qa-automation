"""API client for PeopleHub dashboard endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.dashboard_models import DashboardData, DashboardMeResponse


class Dashboard(Base):
    """API client for PeopleHub dashboard endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the dashboard API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/dashboard"

    def get_dashboard(self) -> CustomResponse[DashboardData, InvalidCredentialsResponse]:
        """Get dashboard statistics."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=DashboardData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_dashboard_me(self) -> CustomResponse[DashboardMeResponse, InvalidCredentialsResponse]:
        """Get dashboard statistics for the current user."""
        return self.request(
            method="GET",
            url=f"{self.url}/me",
            response_model=DashboardMeResponse,
            response_error_model=InvalidCredentialsResponse,
        )
