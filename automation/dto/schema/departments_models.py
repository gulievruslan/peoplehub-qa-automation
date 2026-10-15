
"""DTOs for PeopleHub department API."""

from pydantic import Field, RootModel, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class DepartmentData(PeopleHubDTO):
    """Response DTO for a single department."""

    id: StrictInt = Field(description="Department ID")
    name: StrictStr = Field(description="Department name")


class DepartmentListResponse(RootModel[list[DepartmentData]]):
    """Response DTO for the departments list."""


class DepartmentCreate(PeopleHubDTO):
    """Request DTO for creating a department."""

    name: StrictStr = Field(description="Department name")


class DepartmentUpdate(PeopleHubDTO):
    """Request DTO for updating a department."""

    name: StrictStr = Field(description="Updated department name")
