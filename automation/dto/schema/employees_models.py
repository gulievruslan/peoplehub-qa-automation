"""DTOs for PeopleHub employee API."""
from enum import StrEnum

from pydantic import Field, RootModel, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class EmployeeStatus(StrEnum):
    """Possible employee statuses."""

    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    INACTIVE = "inactive"


class EmployeeData(PeopleHubDTO):
    """Response DTO for a single employee."""

    id: StrictInt = Field(description="Employee ID")
    first_name: StrictStr = Field(description="First name")
    last_name: StrictStr = Field(description="Last name")
    email: StrictStr = Field(description="Email address")
    phone: StrictStr | None = Field(default=None, description="Phone number")
    position: StrictStr = Field(description="Position")
    status: EmployeeStatus = Field(description="Employee status")
    department_id: StrictInt = Field(description="Department ID")
    department_name: StrictStr = Field(description="Department name")
    manager_id: StrictInt | None = Field(default=None, description="Manager ID")
    created_at: StrictStr = Field(description="Creation timestamp")
    updated_at: StrictStr = Field(description="Last update timestamp")


class EmployeeListResponse(RootModel[list[EmployeeData]]):
    """Response DTO for the employees list."""


class EmployeeCreate(PeopleHubDTO):
    """Request DTO for creating an employee."""

    first_name: StrictStr = Field(description="First name")
    last_name: StrictStr = Field(description="Last name")
    email: StrictStr = Field(description="Email address")
    position: StrictStr = Field(description="Position")
    department_id: StrictInt = Field(description="Department ID")
    phone: StrictStr | None = Field(default=None, description="Phone number")
    status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE, description="Employee status")
    manager_id: StrictInt | None = Field(default=None, description="Manager ID")


class EmployeeUpdate(PeopleHubDTO):
    """Request DTO for updating an employee."""

    first_name: StrictStr | None = Field(default=None, description="First name")
    last_name: StrictStr | None = Field(default=None, description="Last name")
    email: StrictStr | None = Field(default=None, description="Email address")
    position: StrictStr | None = Field(default=None, description="Position")
    department_id: StrictInt | None = Field(default=None, description="Department ID")
    phone: StrictStr | None = Field(default=None, description="Phone number")
    status: EmployeeStatus | None = Field(default=None, description="Employee status")
    manager_id: StrictInt | None = Field(default=None, description="Manager ID")
