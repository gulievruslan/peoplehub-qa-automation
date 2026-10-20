from datetime import datetime

from pydantic import AliasPath, BaseModel, ConfigDict, EmailStr, Field

from app.models import EmployeeStatus, LeaveRequestStatus, UserRole


class DepartmentCreate(BaseModel):
    name: str = Field(description="Name of the department.")


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the department.")
    name: str = Field(description="Name of the department.")


class EmployeeCreate(BaseModel):
    first_name: str = Field(description="Employee's first name.")
    last_name: str = Field(description="Employee's last name.")
    email: EmailStr = Field(description="Employee's unique email address.")
    phone: str | None = Field(default=None, description="Employee's phone number.")
    position: str = Field(description="Employee's job title or position.")
    status: EmployeeStatus = Field(
        default=EmployeeStatus.ACTIVE,
        description="Employment status assigned to the employee.",
    )
    department_id: int = Field(description="Identifier of the department the employee belongs to.")
    manager_id: int | None = Field(default=None, description="Identifier of the employee's manager, if assigned.")


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, description="Updated first name of the employee.")
    last_name: str | None = Field(default=None, description="Updated last name of the employee.")
    email: EmailStr | None = Field(default=None, description="Updated email address of the employee.")
    phone: str | None = Field(default=None, description="Updated phone number of the employee.")
    position: str | None = Field(default=None, description="Updated job title or position.")
    status: EmployeeStatus | None = Field(default=None, description="Updated employment status.")
    department_id: int | None = Field(default=None, description="Identifier of the employee's new department.")
    manager_id: int | None = Field(default=None, description="Identifier of the employee's new manager.")


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the employee.")
    first_name: str = Field(description="Employee's first name.")
    last_name: str = Field(description="Employee's last name.")
    email: EmailStr = Field(description="Employee's unique email address.")
    phone: str | None = Field(description="Employee's phone number, if provided.")
    position: str = Field(description="Employee's job title or position.")
    status: EmployeeStatus = Field(description="Current employment status.")
    department_id: int = Field(description="Identifier of the department the employee belongs to.")
    department_name: str = Field(
        validation_alias=AliasPath("department", "name"),
        description="Name of the department the employee belongs to.",
    )
    manager_id: int | None = Field(description="Identifier of the employee's manager, if assigned.")
    created_at: datetime = Field(description="Date and time when the employee record was created.")
    updated_at: datetime = Field(description="Date and time when the employee record was last updated.")


class LeaveRequestCreate(BaseModel):
    employee_id: int = Field(description="Identifier of the employee requesting leave.")
    start_date: datetime = Field(description="Start date and time of the leave period.")
    end_date: datetime = Field(description="End date and time of the leave period.")
    reason: str | None = Field(default=None, description="Reason for the leave request.")


class LeaveRequestUpdate(BaseModel):
    start_date: datetime | None = Field(default=None, description="Updated start date and time of the leave period.")
    end_date: datetime | None = Field(default=None, description="Updated end date and time of the leave period.")
    reason: str | None = Field(default=None, description="Updated reason for the leave request.")
    status: LeaveRequestStatus | None = Field(default=None, description="Updated status of the leave request.")


class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the leave request.")
    employee_id: int = Field(description="Identifier of the employee who submitted the request.")
    start_date: datetime = Field(description="Start date and time of the requested leave.")
    end_date: datetime = Field(description="End date and time of the requested leave.")
    reason: str | None = Field(description="Reason provided for the leave request, if any.")
    status: LeaveRequestStatus = Field(description="Current status of the leave request.")
    created_at: datetime = Field(description="Date and time when the leave request was created.")
    updated_at: datetime = Field(description="Date and time when the leave request was last updated.")


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the notification.")
    user_id: int = Field(description="Identifier of the user who receives the notification.")
    title: str = Field(description="Title of the notification.")
    message: str = Field(description="Notification message content.")
    is_read: bool = Field(description="Indicates whether the notification has been read.")
    created_at: datetime = Field(description="Date and time when the notification was created.")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the user.")
    email: EmailStr = Field(description="User's email address.")
    role: UserRole = Field(description="Role assigned to the user.")
    employee_id: int | None = Field(description="Identifier of the employee linked to this user, if applicable.")


class LoginRequest(BaseModel):
    email: EmailStr = Field(description="Email address used to authenticate the user.")
    password: str = Field(description="Password used to authenticate the user.")


class LoginResponse(BaseModel):
    access_token: str = Field(description="JWT access token issued after successful authentication.")
    token_type: str = Field(description="Type of authentication token, typically Bearer.")


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email address for the new user account.")
    password: str = Field(description="Password for the new user account.")
    role: UserRole = Field(default=UserRole.EMPLOYEE, description="Role assigned to the new user.")
    employee_id: int | None = Field(default=None, description="Identifier of the employee linked to the account.")


class DashboardResponse(BaseModel):
    total_employees: int = Field(description="Total number of employees.")
    active_employees: int = Field(description="Number of employees with active employment status.")
    on_leave_employees: int = Field(description="Number of employees currently on leave.")
    inactive_employees: int = Field(description="Number of employees with inactive employment status.")
    total_departments: int = Field(description="Total number of departments.")
    pending_leave_requests: int = Field(description="Number of leave requests awaiting a decision.")


class PayrollCreate(BaseModel):
    employee_id: int = Field(description="Identifier of the employee receiving the payroll.")
    month: int = Field(description="Payroll month, from 1 to 12.")
    year: int = Field(description="Calendar year for the payroll.")
    salary: float = Field(description="Salary amount for the specified payroll period.")
    status: str = Field(default="pending", description="Payroll payment status.")


class PayrollUpdate(BaseModel):
    month: int | None = Field(default=None, description="Updated payroll month, from 1 to 12.")
    year: int | None = Field(default=None, description="Updated calendar year for the payroll.")
    salary: float | None = Field(default=None, description="Updated salary amount.")
    status: str | None = Field(default=None, description="Updated payroll payment status.")
    paid_at: datetime | None = Field(default=None, description="Date and time when the payroll was paid.")


class PayrollResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique identifier of the payroll record.")
    employee_id: int = Field(description="Identifier of the employee associated with the payroll.")
    month: int = Field(description="Payroll month, from 1 to 12.")
    year: int = Field(description="Calendar year for the payroll.")
    salary: float = Field(description="Salary amount for the payroll period.")
    status: str = Field(description="Current payroll payment status.")
    paid_at: datetime | None = Field(description="Date and time when the payroll was paid, if applicable.")
    created_at: datetime = Field(description="Date and time when the payroll record was created.")
    updated_at: datetime = Field(description="Date and time when the payroll record was last updated.")


class PayrollListResponse(BaseModel):
    items: list[PayrollResponse] = Field(description="List of payroll records.")
    total: int = Field(description="Total number of payroll records matching the query.")
    total_paid: float = Field(description="Total number of payroll records matching the query.")


class PayrollSummaryResponse(BaseModel):
    month: int = Field(description="Month covered by the payroll summary, from 1 to 12.")
    year: int = Field(description="Calendar year covered by the payroll summary.")
    total_payroll: float = Field(description="Combined salary amount for the reporting period.")
    employees_paid: int = Field(description="Number of employees whose payroll has been paid.")
    total_employees: int = Field(description="Total number of employees included in the payroll summary.")
    average_salary: float = Field(description="Average salary for the reporting period.")
    completion_percentage: float = Field(description="Percentage of payrolls completed for the reporting period.")
