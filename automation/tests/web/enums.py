"""Module contains enums for web tests"""
from enum import StrEnum


class DashboardPageTitles(StrEnum):
    """Dashboard page titles."""
    DASHBOARD = "Dashboard"
    PAYROLL_OVERVIEW = "Payroll Overview"
    EMPLOYEE_STATUS = "Employee Status"
    SALARY_BY_EMPLOYEE = "Salary by Employee"


class DashboardPageCards(StrEnum):
    """Dashboard page cards."""
    TOTAL_EMPLOYEES = "Total Employees"
    LEAVE_REQUESTS = "Leave Requests"
    PAYROLL_COMPLETION = "Payroll Completion"
    MONTHLY_PAYROLL_EXPENSES = "Monthly payroll expenses"
    TOTAL_PAYROLL = "Total payroll"
    EMPLOYEES_PAID = "Employees paid"
    AVERAGE_SALARY = "Average salary"
    CURRENT_MONTH_SALARIES = "Current month salaries"
    CURRENT_EMPLOYEE_ACTIVITY = "Current employee activity"


class DepartmentsButtonNames(StrEnum):
    """Departments button names."""
    ADD_DEPARTMENT = "+ Add Department"
    SAVE = "Save"


class LeaveRequestActionButtonNames(StrEnum):
    """LeaveRequest action button names."""
    APPROVE = "Approve"
    REJECT = "Reject"
    EDIT = "Edit"
    DELETE = "Delete"
    CANCEL = 'Cancel'


class SidebarMenuButtonNames(StrEnum):
    """Sidebar menu button names."""
    DASHBOARD = "Dashboard"
    LEAVE_REQUESTS = "Leave Requests"
    EMPLOYEES = "Employees"
    DEPARTMENTS = "Departments"