"""Module contains fixtures for tests"""

import pytest
from _pytest.fixtures import SubRequest, fixture

from automation.api.auth import AuthClient
from automation.config.users import TestUser
from automation.custom.custom_typing import Fixture, FixtureYield
from automation.custom.generators.randoms import get_random_string
from automation.custom.logger.log_fixture import log_fixture
from automation.custom.typed_decorators import typed_title
from automation.dto.schema.auth_models import UserResponse
from automation.tests.api.custom_types import EmployeeData
from automation.tests.api.helper_functions import (
    create_a_new_department,
    create_a_new_employee,
    create_a_new_leave_request,
    create_employee_payroll,
    delete_department_by_id,
    delete_employee_by_id,
    delete_leave_request_by_id,
    delete_payroll_record,
    get_departments_list,
    get_employees_ids_by_name,
    get_leave_requests_ids_by_reason,
    get_payroll_data_by_id,
)
from automation.tests.constants import DEPARTMENT_NAME, FIRST_NAME_RANDOM, LEAVE_REQUEST_RANDOM


@pytest.fixture
@log_fixture
@typed_title(value='Authenticate the specified user')
def get_user_token(request: SubRequest) -> str:
    """Authenticate the specified user.

    Args:
        request (SubRequest): pytest fixture
    """
    user: TestUser = request.param

    response = AuthClient().login(email=user.email, password=user.password.get_secret_value())

    response.check_status_code()

    return response.dto().access_token


@fixture
def create_random_department_name() -> str:
    return DEPARTMENT_NAME.format(random_string=get_random_string())


@fixture
@log_fixture
@typed_title(value='Create a new department and delete after test.')
def create_department_and_delete(
    request: SubRequest, create_random_department_name: Fixture[str]
) -> FixtureYield[int]:
    """Create a new department and delete after test.

    Args:
        request (SubRequest): pytest fixture
        create_random_department_name: create department name fixture
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)

    department_id = create_a_new_department(department_name=create_random_department_name)

    yield department_id

    if need_teardown:
        delete_department_by_id(department_id=department_id)


@fixture
@log_fixture
@typed_title(value='Delete a department after test.')
def delete_department(create_random_department_name: Fixture[str]):
    """Delete a department after test.

    Args:
        create_random_department_name: create department name fixture
    """
    yield

    departments = get_departments_list().root
    department = next(
        (department for department in departments if department.name == create_random_department_name),
        None
    )

    if department:
        delete_department_by_id(department_id=department.id)


@fixture
@log_fixture
@typed_title(value='Create a new employee and delete after test.')
def create_employee_and_delete(
    request: SubRequest, create_department_and_delete: Fixture[int]
) -> FixtureYield[EmployeeData]:
    """Create a new employee and delete after test.

    Args:
        request: Pytest fixture request.
        create_department_and_delete: Fixture that creates a department and deletes it after the test.
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)

    employee_id = create_a_new_employee(department_id=create_department_and_delete)

    yield EmployeeData(employee_id=employee_id, department_id=create_department_and_delete)

    if need_teardown:
        delete_employee_by_id(employee_id=employee_id)


@fixture
def create_employee_first_name() -> str:
    return FIRST_NAME_RANDOM.format(random_string=get_random_string())


@fixture
@log_fixture
@typed_title(value='Delete an employee after test.')
def delete_employee_after_test(create_employee_first_name: str):
    """Delete an employee after test.

    Args:
        create_employee_first_name: creates random employee first name
    """
    yield

    for employee_id in get_employees_ids_by_name(first_name=create_employee_first_name):
        delete_employee_by_id(employee_id=employee_id)


@fixture
def create_employee_leave_request() -> str:
    return LEAVE_REQUEST_RANDOM.format(random_string=get_random_string())

@fixture
@log_fixture
@typed_title(value='Create a new leave request and delete after test.')
def create_leave_request_and_delete(request: SubRequest, create_employee_and_delete: Fixture[EmployeeData]) -> FixtureYield[int]:
    """Create a new leave request and delete after test.

    Args:
        request (SubRequest): pytest fixture
        create_employee_and_delete: create a new employee and delete after test fixture
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)

    leave_request_id = create_a_new_leave_request(
        employee_id=create_employee_and_delete['employee_id'], reason=request.param.get('reason')
    )

    yield leave_request_id

    if need_teardown:
        delete_leave_request_by_id(leave_request_id=leave_request_id)


@fixture
@log_fixture
@typed_title(value='Delete a leave request after test.')
def delete_leave_request_after_test(create_employee_leave_request: Fixture[str]) -> FixtureYield[None]:
    """Delete a leave request after test.

    Args:
        create_employee_leave_request: leave request reason
    """
    yield

    leave_request_ids = get_leave_requests_ids_by_reason(reason=create_employee_leave_request)

    for leave_request_id in leave_request_ids:
        delete_leave_request_by_id(leave_request_id=leave_request_id)


@fixture
@log_fixture
@typed_title(value='Get my information')
def get_my_information(request: SubRequest) -> UserResponse:
    """Get my information

    Args:
        request (SubRequest): pytest fixture
    """
    user: TestUser = request.param

    response = AuthClient(requires_auth=True, user=user).get_me()

    response.check_status_code()

    return response.dto()


@fixture
@log_fixture
@typed_title(value='Create payroll record and delete after test.')
def create_payroll_record_and_delete_after_test(
    request: SubRequest, create_employee_and_delete: Fixture[EmployeeData]
) -> FixtureYield[int]:
    """Create a new payroll record and delete after test.

    Args:
        request (SubRequest): pytest fixture
        create_employee_and_delete: create a new employee and delete after test fixture
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)

    payroll_id = create_employee_payroll(employee_id=create_employee_and_delete['employee_id'])

    yield payroll_id

    if need_teardown:
        delete_payroll_record(payroll_id=payroll_id)


@fixture
@log_fixture
@typed_title(value='Delete payroll after test')
def delete_payroll_after_test(
    request: SubRequest, create_employee_and_delete: Fixture[EmployeeData]
) -> FixtureYield[None]:
    """Delete payroll after test.

    Args:
        request (SubRequest): pytest fixture
        create_employee_and_delete: create a new employee and delete after test fixture
    """
    yield

    for payroll_id in get_payroll_data_by_id(employee_id=create_employee_and_delete['employee_id']):
        delete_payroll_record(payroll_id=payroll_id)
