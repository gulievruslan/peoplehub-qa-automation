"""API client for PeopleHub health endpoints."""
from typing import Any

from automation.custom.request.base_api import BaseApi
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.health_models import DatabaseHealthResponse, HealthResponse


class Health(BaseApi):
    """API client for PeopleHub health endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the health API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)

    def get_health(self) -> CustomResponse[HealthResponse, None]:
        """Check application health."""
        return self.request(
            method="GET",
            url=f"{self.url}/health",
            response_model=HealthResponse,
        )

    def get_database_health(self) -> CustomResponse[DatabaseHealthResponse, None]:
        """Check database health."""
        return self.request(
            method="GET",
            url=f"{self.url}/health/db",
            response_model=DatabaseHealthResponse,
        )
