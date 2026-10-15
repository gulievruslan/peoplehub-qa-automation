"""Module contains helper functions for fixtures"""

from automation.api.departments import Departments
from automation.api.employees import Employees
from automation.api.leave_requests import LeaveRequests
from automation.api.payroll import Payroll
from automation.config.users import ADMIN
from automation.custom.allure.custom_allure import step
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.custom.generators.randoms import (
    get_random_email,
    get_random_number,
    get_random_phone,
    get_random_string,
)
from automation.dto.schema.departments_models import DepartmentListResponse
from automation.dto.schema.employees_models import EmployeeStatus


@step('Create a new department')
def create_a_new_department(department_name: str) -> int:
    """Create a department

    Args:
        department_name: department name
    """
    response = Departments(user=ADMIN).post_department(name=department_name)

    response.check_status_code(expected_code=201)

    return response.dto().id


@step('Get departments list')
def get_departments_list() -> DepartmentListResponse:
    """Get departments list"""
    response = Departments(user=ADMIN).get_departments()

    response.check_status_code()

    return response.dto()


@step('Delete department by id')
def delete_department_by_id(department_id: int):
    """Delete a department by id

    Args:
        department_id: department id
    """
    response = Departments(user=ADMIN).delete_department(department_id=department_id)

    response.check_status_code(expected_code=204)


@step('Create a new employee')
def create_a_new_employee(department_id: int) -> int:
    """Create a new employee

    Args:
        department_id: department id
    """
    response = Employees(user=ADMIN).post_employee(
        first_name=f"first_name_by_fixture {get_random_string()}",
        last_name=f"last_name_by_fixture {get_random_string()}",
        email=get_random_email(),
        position=f'Position_by_AT {get_random_string()}',
        department_id=department_id,
        phone=get_random_phone(),
        status=EmployeeStatus.ACTIVE,
    )

    response.check_status_code(expected_code=201)

    return response.dto().id


@step('Delete an employee by id')
def delete_employee_by_id(employee_id: int):
    """Delete an employee by id

    Args:
        employee_id: employee id
    """
    response = Employees(user=ADMIN).delete_employee(employee_id=employee_id)

    response.check_status_code(expected_code=204)


@step('Get employees id by firstname')
def get_employees_ids_by_name(first_name: str) -> tuple[int, ...]:
    """Get employees list

    Args:
        first_name: employee firstname
    """
    response = Employees(user=ADMIN).get_employees()

    response.check_status_code()

    return tuple(employee.id for employee in response.dto().root if first_name == employee.first_name)


@step('Create leave request')
def create_a_new_leave_request(employee_id: int, reason: str) -> int:
    """Create a new leave request

    Args:
        employee_id: employee's id
        reason: leave request reason
    """
    response = LeaveRequests(user=ADMIN).post_leave_request(
        employee_id=employee_id,
        start_date=CustomDateTime().get_offset_string(),
        end_date=CustomDateTime().get_offset_string(days=get_random_number(end=30)),
        reason=reason
    )

    response.check_status_code(expected_code=201)

    return response.dto().id


@step('Get leave requests ids by reason')
def get_leave_requests_ids_by_reason(reason: str) -> tuple[int, ...]:
    """Get leave requests ids by reason

    Args:
        reason: leave requests reason
    """
    response = LeaveRequests(user=ADMIN).get_leave_requests()

    response.check_status_code()

    return tuple(request.id for request in response.dto().root if reason == request.reason)


@step('Delete leave request by id')
def delete_leave_request_by_id(leave_request_id: int):
    """Delete leave request by id

    Args:
        leave_request_id: leave request id
    """
    response = LeaveRequests(user=ADMIN).delete_leave_request(leave_request_id=leave_request_id)

    response.check_status_code(expected_code=204)


@step('Create employee payroll')
def create_employee_payroll(employee_id: int) -> int:
    """Create employee payroll

    Args:
        employee_id: employee id
    """
    response = Payroll(user=ADMIN).post_payroll(
        employee_id=employee_id,
        month=CustomDateTime().month,
        year=CustomDateTime().year,
        salary=get_random_number(end=4000)
    )

    response.check_status_code(expected_code=201)

    return response.dto().id


@step('Get payroll data')
def get_payroll_data_by_id(employee_id: int) -> tuple[int]:
    """Get payroll data

    Args:
        employee_id: employee id
    """
    response = Payroll(user=ADMIN).get_payroll()

    response.check_status_code()

    return tuple(payroll.id for payroll in response.dto().items if payroll.employee_id == employee_id)


@step('Delete payroll record')
def delete_payroll_record(payroll_id: int):
    """Delete payroll record

    Args:
        payroll_id: payroll record id
    """
    response = Payroll(user=ADMIN).delete_payroll(payroll_id=payroll_id)

    response.check_status_code(expected_code=204)
