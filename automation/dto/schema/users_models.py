
"""DTOs for PeopleHub user API."""

from pydantic import Field, StrictInt

from automation.dto.schema.generic import PeopleHubDTO


class EmployeeLinkRequest(PeopleHubDTO):
    """Request DTO for linking a user to an employee."""

    employee_id: StrictInt | None = Field(description="Employee ID to link to the user")
