
"""DTOs for PeopleHub dashboard API."""

from pydantic import Field, RootModel, StrictInt

from automation.dto.schema.generic import PeopleHubDTO


class DashboardData(PeopleHubDTO):
    """Response DTO for dashboard statistics."""

    total_employees: StrictInt = Field(description="Total number of employees")
    active_employees: StrictInt = Field(description="Number of active employees")
    on_leave_employees: StrictInt = Field(description="Number of employees on leave")
    inactive_employees: StrictInt = Field(description="Number of inactive employees")
    total_departments: StrictInt = Field(description="Total number of departments")
    pending_leave_requests: StrictInt = Field(description="Number of pending leave requests")


class DashboardMeResponse(PeopleHubDTO):
    """Response DTO for current-user dashboard statistics."""
    total_leave_requests: StrictInt = Field()
    pending_leave_requests: StrictInt = Field()
    approved_leave_requests: StrictInt = Field()
