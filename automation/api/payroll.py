"""API client for PeopleHub payroll endpoints."""
from datetime import datetime
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.payroll_models import (
    PayrollData,
    PayrollListResponse,
    PayrollSummaryData,
    PayrollSummaryListResponse,
)


class Payroll(Base):
    """API client for PeopleHub payroll endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the payroll API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/payroll"

    def get_payroll(self) -> CustomResponse[PayrollListResponse, InvalidCredentialsResponse]:
        """Get the payroll list."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=PayrollListResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def post_payroll(
        self,
        employee_id: int,
        month: int,
        year: int,
        salary: float,
        status: str = "pending",
    ) -> CustomResponse[PayrollData, InvalidCredentialsResponse]:
        """Create a payroll record.

        Args:
            employee_id: ID of the employee.
            month: Payroll month.
            year: Payroll year.
            salary: Salary amount.
            status: Payroll status. Defaults to pending.
        """

        return self.request(
            method="POST",
            url=self.url,
            json={
                "employee_id": employee_id,
                "month": month,
                "year": year,
                "salary": salary,
                "status": status,
            },
            response_model=PayrollData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_payroll_by_employee(self) -> CustomResponse:
        """Get payroll data grouped or filtered by employee."""
        return self.request(method="GET", url=f"{self.url}/by-employee")

    def get_payroll_history(self) -> CustomResponse[PayrollSummaryListResponse, InvalidCredentialsResponse]:
        """Get payroll summary history."""
        return self.request(
            method="GET",
            url=f"{self.url}/history",
            response_model=PayrollSummaryListResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_payroll_summary(self) -> CustomResponse[PayrollSummaryData, InvalidCredentialsResponse]:
        """Get the payroll summary."""
        return self.request(
            method="GET",
            url=f"{self.url}/summary",
            response_model=PayrollSummaryData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_payroll_by_id(
        self,
        payroll_id: int,
    ) -> CustomResponse[PayrollData, InvalidCredentialsResponse]:
        """Get a payroll record by ID.

        Args:
            payroll_id: ID of the payroll record to retrieve.
        """
        return self.request(
            method="GET",
            url=f"{self.url}/{payroll_id}",
            response_model=PayrollData,
            response_error_model=InvalidCredentialsResponse,
        )

    def update_payroll(
        self,
        payroll_id: int,
        month: int | None = None,
        year: int | None = None,
        salary: float | None = None,
        status: str | None = None,
        paid_at: datetime | None = None,
    ) -> CustomResponse[PayrollData, InvalidCredentialsResponse]:
        """Update a payroll record.

        Args:
            payroll_id: ID of the payroll record to update.
            month: Updated payroll month.
            year: Updated payroll year.
            salary: Updated salary amount.
            status: Updated payroll status.
            paid_at: Payment timestamp.
        """
        return self.request(
            method="PATCH",
            url=f"{self.url}/{payroll_id}",
            json={
                "month": month,
                "year": year,
                "salary": salary,
                "status": status,
                "paid_at": paid_at,
            },
            response_model=PayrollData,
            response_error_model=InvalidCredentialsResponse,
        )

    def delete_payroll(self, payroll_id: int) -> CustomResponse:
        """Delete a payroll record.

        Args:
            payroll_id: ID of the payroll record to delete.
        """
        return self.request(method="DELETE", url=f"{self.url}/{payroll_id}")
