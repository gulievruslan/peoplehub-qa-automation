"""Module contains fixtures for automation tests"""
from collections import Counter

import allure
from _pytest.fixtures import SubRequest
from pytest import fixture

from automation.api.leave_requests import LeaveRequests
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture, FixtureYield
from automation.custom.generators.randoms import get_random_string
from automation.custom.logger.log_fixture import log_fixture
from automation.custom.typed_decorators import typed_title
from automation.dto.schema.auth_models import UserResponse
from automation.dto.schema.leave_requests_models import LeaveRequestStatus
from automation.dto.schema.payroll_models import PayrollListResponse
from automation.tests.constants import DEPARTMENT_NAME, FIRST_NAME_RANDOM, LEAVE_REQUEST_RANDOM
from automation.tests.custom_types import DepartmentParams, EmployeeParams, LeaveRequestParams, LeaveRequestStatusCounts
from automation.tests.helper_functions import (
    create_a_new_department,
    create_a_new_employee,
    create_a_new_leave_request,
    create_employee_payroll,
    delete_department_by_id,
    delete_employee_by_id,
    delete_leave_request_by_id,
    delete_payroll_record,
    get_departments_list,
    get_employee_payroll_data,
    get_employees_history,
    get_employees_ids_by_name,
    get_info_about_me,
    get_leave_requests_ids_by_reason,
    get_payroll_data,
    get_payroll_data_by_id,
)

QASE_PROJECT_CODE = "PEOPLEHUB"
QASE_CASE_URL = "https://app.qase.io/case/{project_code}-{case_id}"


def pytest_runtest_setup(item):
    qase_marker = item.get_closest_marker("qase_id")
    if qase_marker is None:
        return

    case_id = qase_marker.kwargs.get("id")

    if case_id is None:
        return

    allure.dynamic.link(
        QASE_CASE_URL.format(project_code=QASE_PROJECT_CODE, case_id=case_id),
        link_type="test_case",
        name=f"Qase: {QASE_PROJECT_CODE}-{case_id}",
    )


@fixture
def create_random_department_name() -> str:
    return DEPARTMENT_NAME.format(random_string=get_random_string())


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
@typed_title(value='Create a new department and delete after test.')
def create_department_and_delete(
    request: SubRequest, create_random_department_name: Fixture[str]
) -> FixtureYield[DepartmentParams]:
    """Create a new department and delete after test.

    Args:
        request: subrequest
        create_random_department_name: create department name fixture
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)
    department_name = getattr(request, "param", {}).get("department_name")

    department_data = create_a_new_department(department_name=department_name or create_random_department_name)

    yield department_data

    if need_teardown:
        delete_department_by_id(department_id=department_data['department_id'])


@fixture
@log_fixture
@typed_title(value='Create a new employee and delete after test.')
def create_employee_and_delete(
    request: SubRequest, create_department_and_delete: Fixture[DepartmentParams]
) -> FixtureYield[EmployeeParams]:
    """Create a new employee and delete after test.

    Args:
        request: subrequest
        create_department_and_delete: Fixture that creates a department and deletes it after the test.
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)

    employee_data = create_a_new_employee(department_id=create_department_and_delete['department_id'])

    yield EmployeeParams(
        employee_id=employee_data.id,
        department_id=employee_data.department_id,
        department_name=employee_data.department_name,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        position=employee_data.position,
        phone=employee_data.phone,
        status=employee_data.status,
        email=employee_data.email
    )

    if need_teardown:
        delete_employee_by_id(employee_id=employee_data.id)


@fixture
def create_employee_first_name() -> str:
    return FIRST_NAME_RANDOM.format(random_string=get_random_string())


@fixture
@log_fixture
@typed_title(value='Delete an employee after test.')
def delete_employee_after_test(create_employee_first_name: Fixture[str]) -> FixtureYield[None]:
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
def create_leave_request_and_delete(
    request: SubRequest,
    create_employee_leave_request: Fixture[str],
    create_employee_and_delete: Fixture[EmployeeParams]
) -> FixtureYield[LeaveRequestParams]:
    """Create a new leave request and delete after test.

    Args:
        request: subrequest
        create_employee_leave_request: random leave request name fixture
        create_employee_and_delete: create a new employee and delete after test fixture
    """
    need_teardown = getattr(request, "param", {}).get("need_teardown", True)
    reason = getattr(request, "param", {}).get("reason", create_employee_leave_request)
    user = getattr(request, "param", {}).get("user", ADMIN)

    leave_request_data = create_a_new_leave_request(
        employee_id=(
            create_employee_and_delete['employee_id'] if user == ADMIN else get_info_about_me(user=user).employee_id
        ),
        reason=reason,
        user=user
    )

    yield LeaveRequestParams(
        first_name=create_employee_and_delete['first_name'],
        last_name=create_employee_and_delete['last_name'],
        leave_request_id=leave_request_data.id,
        start_date=leave_request_data.start_date,
        end_date=leave_request_data.end_date,
        reason=leave_request_data.reason,
        status=leave_request_data.status,
    )

    if need_teardown:
        delete_leave_request_by_id(leave_request_id=leave_request_data.id)


@fixture
@log_fixture
@typed_title(value='Delete a leave request after test.')
def delete_leave_request_after_test(request: SubRequest, create_employee_leave_request: Fixture[str]) -> FixtureYield[
    None]:
    """Delete a leave request after test.

    Args:
        request: subrequest
        create_employee_leave_request: leave request reason
    """
    yield

    reason = getattr(request, "param", {}).get("reason", create_employee_leave_request)

    leave_request_ids = get_leave_requests_ids_by_reason(reason=reason)

    for leave_request_id in leave_request_ids:
        delete_leave_request_by_id(leave_request_id=leave_request_id)


@fixture
@log_fixture
@typed_title(value='Create payroll record and delete after test.')
def create_payroll_record_and_delete_after_test(
    request: SubRequest, create_employee_and_delete: Fixture[EmployeeParams]
) -> FixtureYield[int]:
    """Create a new payroll record and delete after test.

    Args:
        request: subrequest
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
    request: SubRequest, create_employee_and_delete: Fixture[EmployeeParams]
) -> FixtureYield[None]:
    """Delete payroll after test.

    Args:
        request: subrequest
        create_employee_and_delete: create a new employee and delete after test fixture
    """
    yield

    for payroll_id in get_payroll_data_by_id(employee_id=create_employee_and_delete['employee_id']):
        delete_payroll_record(payroll_id=payroll_id)


@fixture
@log_fixture
@typed_title(value='Get leave requests status counts')
def get_leave_request_status_counts() -> LeaveRequestStatusCounts:
    """Return the number of leave requests for each status."""
    response = LeaveRequests(user=ADMIN).get_leave_requests()

    response.check_status_code()

    status_counts = Counter(request.status for request in response.dto().root)

    return LeaveRequestStatusCounts(
        approved=status_counts.get(LeaveRequestStatus.APPROVED, 0),
        pending=status_counts.get(LeaveRequestStatus.PENDING, 0),
        rejected=status_counts.get(LeaveRequestStatus.REJECTED, 0),
    )


@fixture
@log_fixture
@typed_title(value='Get my information')
def get_my_information(request: SubRequest) -> UserResponse:
    """Get my information

    Args:
        request: subrequest
    """
    return get_info_about_me(user=request.param)


@fixture
@log_fixture
@typed_title(value='Get payroll data by employee')
def get_payroll_data_by_employee() -> dict[str, int | float]:
    """Get payroll data by employee"""
    return {employee.employee_name: employee.salary for employee in get_employee_payroll_data()}


@fixture
@log_fixture
@typed_title(value="Get payroll history")
def get_payroll_history() -> dict[str, float | int]:
    """Get payroll history."""
    payroll = get_employees_history()[-1]

    return {
        "total_payroll": payroll.total_payroll,
        "employees_paid": payroll.employees_paid,
        "average_salary": payroll.average_salary,
    }

@fixture
@log_fixture
@typed_title(value='Get payroll data')
def get_all_payroll_data() -> PayrollListResponse:
    """Get payroll data"""
    return get_payroll_data()