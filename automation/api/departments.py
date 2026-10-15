"""API client for PeopleHub department endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.departments_models import DepartmentData, DepartmentListResponse


class Departments(Base):
    """API client for PeopleHub department endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the departments API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/departments"

    def get_departments(self) -> CustomResponse[DepartmentListResponse, InvalidCredentialsResponse]:
        """Get the departments list."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=DepartmentListResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def post_department(self, name: str) -> CustomResponse[DepartmentData, InvalidCredentialsResponse]:
        """Create a department.

        Args:
            name: Name of the department to create.
        """
        return self.request(
            method="POST",
            url=self.url,
            json={"name": name},
            response_model=DepartmentData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_department_by_id(
        self,
        department_id: int,
    ) -> CustomResponse[DepartmentData, InvalidCredentialsResponse]:
        """Get a department by ID.

        Args:
            department_id: ID of the department to retrieve.
        """
        return self.request(
            method="GET",
            url=f"{self.url}/{department_id}",
            response_model=DepartmentData,
            response_error_model=InvalidCredentialsResponse,
        )

    def update_department(
        self,
        department_id: int,
        department_name: str,
    ) -> CustomResponse[DepartmentData, InvalidCredentialsResponse]:
        """Update a department.

        Args:
            department_id: ID of the department to update.
            department_name: Updated department name.
        """
        return self.request(
            method="PUT",
            url=f"{self.url}/{department_id}",
            json={"name": department_name},
            response_model=DepartmentData,
            response_error_model=InvalidCredentialsResponse,
        )

    def delete_department(self, department_id: int) -> CustomResponse:
        """Delete a department.

        Args:
            department_id: ID of the department to delete.
        """
        return self.request(method="DELETE", url=f"{self.url}/{department_id}")
