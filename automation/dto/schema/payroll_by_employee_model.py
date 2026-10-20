"""DTOs for PeopleHub payroll by employee API."""
from pydantic import Field, RootModel, StrictFloat, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class PayrollByEmployeeData(PeopleHubDTO):
    """Response DTO for a single payroll record."""
    employee_id: StrictInt = Field(description="Employee ID")
    employee_name: StrictStr = Field(description="Employee Name")
    salary: StrictFloat = Field(description="Salary")


class PayrollByEmployee(RootModel[list[PayrollByEmployeeData]]):
    """Response DTO for a list of payroll records."""
