"""DTOs for PeopleHub health endpoints."""

from pydantic import StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class HealthResponse(PeopleHubDTO):
    """Response DTO for application health."""
    status: StrictStr

class DatabaseHealthResponse(PeopleHubDTO):
    """Response DTO for database health."""
    database: StrictStr
