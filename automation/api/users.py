"""API client for PeopleHub user endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse, UserResponse
from automation.dto.schema.users_models import EmployeeLinkRequest


class Users(Base):
    """API client for PeopleHub user endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the users API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/users"

    def link_employee(
        self,
        user_id: int,
        employee_id: int | None,
    ) -> CustomResponse[UserResponse, InvalidCredentialsResponse]:
        """Link or unlink an employee from a user.

        Args:
            user_id: ID of the user to update.
            employee_id: Employee ID to link, or None to unlink.
        """
        return self.request(
            method="PATCH",
            url=f"{self.url}/{user_id}/employee",
            json=EmployeeLinkRequest(employee_id=employee_id),
            response_model=UserResponse,
            response_error_model=InvalidCredentialsResponse,
        )
