"""DTOs for PeopleHub payroll API."""

from datetime import datetime

from pydantic import Field, RootModel, StrictFloat, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class PayrollData(PeopleHubDTO):
    """Response DTO for a single payroll record."""

    id: StrictInt = Field(description="Payroll record ID")
    employee_id: StrictInt = Field(description="Employee ID")
    month: StrictInt = Field(description="Payroll month")
    year: StrictInt = Field(description="Payroll year")
    salary: float = Field(description="Salary amount")
    status: StrictStr = Field(description="Payroll status")
    paid_at: datetime | None = Field(default=None, description="Payment timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class PayrollListResponse(PeopleHubDTO):
    """Response DTO for the payroll list."""

    items: list[PayrollData] = Field(description="Payroll records")
    total_paid: StrictFloat = Field(description="Total number of payroll records matching the query.")
    total: StrictInt = Field(description="Total number of payroll records")


class PayrollSummaryData(PeopleHubDTO):
    """Response DTO for payroll summary statistics."""

    month: StrictInt = Field(description="Payroll month")
    year: StrictInt = Field(description="Payroll year")
    total_payroll: float = Field(description="Total payroll amount")
    employees_paid: StrictInt = Field(description="Number of employees paid")
    total_employees: StrictInt = Field(description="Total number of employees")
    average_salary: float = Field(description="Average salary")
    completion_percentage: float = Field(description="Payroll completion percentage")


class PayrollSummaryListResponse(RootModel[list[PayrollSummaryData]]):
    """Response DTO for payroll summary history."""


class PayrollCreate(PeopleHubDTO):
    """Request DTO for creating a payroll record."""

    employee_id: StrictInt = Field(description="Employee ID")
    month: StrictInt = Field(description="Payroll month")
    year: StrictInt = Field(description="Payroll year")
    salary: float = Field(description="Salary amount")
    status: StrictStr = Field(default="pending", description="Payroll status")


class PayrollUpdate(PeopleHubDTO):
    """Request DTO for updating a payroll record."""

    month: StrictInt | None = Field(default=None, description="Payroll month")
    year: StrictInt | None = Field(default=None, description="Payroll year")
    salary: float | None = Field(default=None, description="Salary amount")
    status: StrictStr | None = Field(default=None, description="Payroll status")
    paid_at: datetime | None = Field(default=None, description="Payment timestamp")


class PayrollItemInfo(PeopleHubDTO):
    """DTO containing the month, status, and salary of a payroll record."""

    month: StrictStr = Field(description="Payroll month")
    year: StrictInt = Field(description="Payroll year")
    status: StrictStr = Field(description="Payroll status")
    salary: float = Field(description="Salary amount")
