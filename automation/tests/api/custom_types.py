"""Module contains custom types"""
from typing import TypedDict


class AuthData(TypedDict):
    """Authentication data type"""
    email: str
    password: str


class EmployeeData(TypedDict):
    """Employee data type"""
    employee_id: int
    department_id: int