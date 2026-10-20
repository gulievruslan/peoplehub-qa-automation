"""Module contains custom types"""
from typing import TypedDict


class AuthParams(TypedDict):
    """Authentication parameters type"""
    email: str
    password: str


class EmployeeParams(TypedDict):
    """Employee parameters type"""
    employee_id: int
    department_id: int
    department_name: str
    first_name: str
    last_name: str
    position: str
    status: str
    email: str
    phone: str | None


class DepartmentParams(TypedDict):
    """Department parameters type"""
    department_id: int
    department_name: str


class LeaveRequestParams(TypedDict):
    """LeaveRequest parameters type"""
    first_name: str
    last_name: str
    leave_request_id: int
    start_date: str
    end_date: str
    reason: str | None
    status: str


class LeaveRequestStatusCounts(TypedDict, total=False):
    """Number of leave requests grouped by status."""
    approved: int
    pending: int
    rejected: int


class EmployeeData(TypedDict):
    """Employee data type"""
    employee_name: str
    employee_salary: int | float