from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import EmployeeStatus, LeaveRequestStatus, UserRole


class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    position: str
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    department_id: int
    manager_id: int | None = None


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    position: str | None = None
    status: EmployeeStatus | None = None
    department_id: int | None = None
    manager_id: int | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    position: str
    status: EmployeeStatus
    department_id: int
    manager_id: int | None
    created_at: datetime
    updated_at: datetime


class LeaveRequestCreate(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: str | None = None


class LeaveRequestUpdate(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    reason: str | None = None
    status: LeaveRequestStatus | None = None


class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: str | None
    status: LeaveRequestStatus
    created_at: datetime
    updated_at: datetime


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    employee_id: int | None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.EMPLOYEE
    employee_id: int | None = None


class DashboardResponse(BaseModel):
    total_employees: int
    active_employees: int
    on_leave_employees: int
    inactive_employees: int
    total_departments: int
    pending_leave_requests: int


class PayrollCreate(BaseModel):
    employee_id: int
    month: int
    year: int
    salary: float
    status: str = "pending"


class PayrollUpdate(BaseModel):
    month: int | None = None
    year: int | None = None
    salary: float | None = None
    status: str | None = None
    paid_at: datetime | None = None


class PayrollResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    month: int
    year: int
    salary: float
    status: str
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PayrollListResponse(BaseModel):
    total: int
    items: list[PayrollResponse]


class PayrollSummaryResponse(BaseModel):
    month: int
    year: int
    total_payroll: float
    employees_paid: int
    total_employees: int
    average_salary: float
    completion_percentage: float