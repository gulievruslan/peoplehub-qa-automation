
"""DTOs for PeopleHub leave request API."""
from enum import StrEnum

from pydantic import Field, RootModel, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class LeaveRequestStatus(StrEnum):
    """Possible leave request statuses."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveRequestData(PeopleHubDTO):
    """Response DTO for a single leave request."""

    id: StrictInt = Field(description="Leave request ID")
    employee_id: StrictInt = Field(description="Employee ID")
    start_date: StrictStr = Field(description="Leave start date")
    end_date: StrictStr = Field(description="Leave end date")
    reason: StrictStr | None = Field(default=None, description="Reason for leave")
    status: LeaveRequestStatus = Field(description="Leave request status")
    created_at: StrictStr = Field(description="Creation timestamp")
    updated_at: StrictStr = Field(description="Last update timestamp")


class LeaveRequestListResponse(RootModel[list[LeaveRequestData]]):
    """Response DTO for the leave requests list."""


class LeaveRequestCreate(PeopleHubDTO):
    """Request DTO for creating a leave request."""

    employee_id: StrictInt = Field(description="Employee ID")
    start_date: StrictStr = Field(description="Leave start date")
    end_date: StrictStr = Field(description="Leave end date")
    reason: StrictStr | None = Field(default=None, description="Reason for leave")


class LeaveRequestUpdate(PeopleHubDTO):
    """Request DTO for updating a leave request."""

    start_date: StrictStr | None = Field(default=None, description="Leave start date")
    end_date: StrictStr | None = Field(default=None, description="Leave end date")
    reason: StrictStr | None = Field(default=None, description="Reason for leave")
    status: LeaveRequestStatus | None = Field(default=None, description="Leave request status")
