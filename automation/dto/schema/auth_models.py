"""DTOs for PeopleHub authentication API."""

from enum import StrEnum
from typing import Any

from pydantic import EmailStr, StrictInt, StrictStr, Field

from automation.dto.schema.generic import PeopleHubDTO


class UserRole(StrEnum):
    """Supported PeopleHub user roles."""
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    EMPLOYEE = "employee"


class LoginResponse(PeopleHubDTO):
    """Response DTO returned after successful authentication."""
    access_token: StrictStr
    token_type: StrictStr


class UserResponse(PeopleHubDTO):
    """Response DTO for the authenticated user."""
    id: StrictInt = Field(description="User ID.")
    email: EmailStr = Field(description="User email.")
    role: UserRole = Field(description="User role.")
    employee_id: StrictInt = Field(description="User employee ID.")


class Ctx(PeopleHubDTO):
    """Additional context returned in a validation error."""
    reason: StrictStr | None = None


class InvalidEmailResponse(PeopleHubDTO):
    """Response DTO for a validation error."""
    type: StrictStr = Field(description="Issue type.")
    loc: list[StrictStr | StrictInt] = Field(description="Error location.")
    msg: StrictStr = Field(description="Error message.")
    input: Any = None
    ctx: dict[str, Any] | Ctx | None = None


class InvalidCredentialsResponse(PeopleHubDTO):
    """Response DTO for an authentication or validation error."""
    detail: StrictStr | list[InvalidEmailResponse]
