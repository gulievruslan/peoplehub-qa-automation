"""API client for PeopleHub employee endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.employees_models import EmployeeData, EmployeeListResponse, EmployeeStatus


class Employees(Base):
    """API client for PeopleHub employee endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the employees API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/employees"

    def get_employees(self) -> CustomResponse[EmployeeListResponse, InvalidCredentialsResponse]:
        """Get the employees list."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=EmployeeListResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def post_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        position: str,
        department_id: int,
        phone: str | None = None,
        status: EmployeeStatus | None = None,
        manager_id: int | None = None,
    ) -> CustomResponse[EmployeeData, InvalidCredentialsResponse]:
        """Create an employee.

        Args:
            first_name: Employee's first name.
            last_name: Employee's last name.
            email: Employee's email address.
            position: Employee's job position.
            department_id: ID of the employee's department.
            phone: Employee's phone number.
            status: Employee's status. Defaults to active.
            manager_id: ID of the employee's manager.
        """
        return self.request(
            method="POST",
            url=self.url,
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "position": position,
                "department_id": department_id,
                "phone": phone,
                "status": status if status is not None else EmployeeStatus.ACTIVE,
                "manager_id": manager_id,
            },
            response_model=EmployeeData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_employee_by_id(
        self,
        employee_id: int,
    ) -> CustomResponse[EmployeeData, InvalidCredentialsResponse]:
        """Get an employee by ID.

        Args:
            employee_id: ID of the employee to retrieve.
        """
        return self.request(
            method="GET",
            url=f"{self.url}/{employee_id}",
            response_model=EmployeeData,
            response_error_model=InvalidCredentialsResponse,
        )

    def update_employee(
        self,
        employee_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        position: str | None = None,
        department_id: int | None = None,
        phone: str | None = None,
        status: EmployeeStatus | None = None,
        manager_id: int | None = None,
    ) -> CustomResponse[EmployeeData, InvalidCredentialsResponse]:
        """Update an employee.

        Args:
            employee_id: ID of the employee to update.
            first_name: Updated first name.
            last_name: Updated last name.
            email: Updated email address.
            position: Updated job position.
            department_id: Updated department ID.
            phone: Updated phone number.
            status: Updated employee status.
            manager_id: Updated manager ID.
        """
        return self.request(
            method="PUT",
            url=f"{self.url}/{employee_id}",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "position": position,
                "department_id": department_id,
                "phone": phone,
                "status": status if status is not None else EmployeeStatus.ACTIVE,
                "manager_id": manager_id,
            },
            response_model=EmployeeData,
            response_error_model=InvalidCredentialsResponse,
        )

    def delete_employee(self, employee_id: int) -> CustomResponse:
        """Delete an employee.

        Args:
            employee_id: ID of the employee to delete.
        """
        return self.request(method="DELETE", url=f"{self.url}/{employee_id}")
