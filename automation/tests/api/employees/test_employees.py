from allure import story
from pytest import mark

from automation.api.employees import Employees
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.generators.randoms import get_random_email, get_random_phone, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.dto.schema.employees_models import EmployeeStatus
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.constants import FIRST_NAME_RANDOM
from automation.tests.custom_types import DepartmentParams, EmployeeParams


@story("Employees")
@mark.employees
class TestEmployees(PeopleHubApi):

    @typed_qase_id(qase_id=60)
    @typed_title(value="Get employees list")
    def test_get_employees_list(self):
        response = Employees(user=ADMIN).get_employees()

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=61)
    @typed_title(value="Create employee with valid data")
    def test_create_employee(
        self,
        create_employee_first_name: Fixture[str],
        create_department_and_delete: Fixture[DepartmentParams],
        delete_employee_after_test: Fixture[None]
    ):
        response = Employees(user=ADMIN).post_employee(
            first_name=create_employee_first_name,
            last_name=f"last_name_by_AT {get_random_string()}",
            email=get_random_email(),
            position=f"Position_by_AT {get_random_string()}",
            department_id=create_department_and_delete['department_id'],
            phone=get_random_phone(),
            status=EmployeeStatus.ACTIVE,
        )

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()

    @typed_qase_id(qase_id=62)
    @typed_title(value="Get employee by ID")
    def test_get_employee_by_id(self, create_employee_and_delete: Fixture[EmployeeParams]):
        response = Employees(user=ADMIN).get_employee_by_id(
            employee_id=create_employee_and_delete['employee_id'],
        )

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=147)
    @typed_title(value="Delete employee")
    @mark.parametrize("create_employee_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_employee(self, create_employee_and_delete: Fixture[EmployeeParams]):
        response = Employees(user=ADMIN).delete_employee(employee_id=create_employee_and_delete['employee_id'])

        response.assert_status_code(expected_code=204)

    @typed_qase_id(qase_id=149)
    @typed_title(value="Update employee")
    def test_update_employee(self, create_employee_and_delete: Fixture[EmployeeParams]):
        response = Employees(user=ADMIN).update_employee(
            first_name=FIRST_NAME_RANDOM.format(random_string=get_random_string()),
            last_name=f"updated_last_name_by_AT {get_random_string()}",
            email=get_random_email(),
            position=f"Updated position_by_AT {get_random_string()}",
            employee_id=create_employee_and_delete['employee_id'],
            department_id=create_employee_and_delete['department_id'],
            phone=get_random_phone(),
            status=EmployeeStatus.ON_LEAVE,
        )

        response.assert_status_code()
        response.assert_model_valid()
