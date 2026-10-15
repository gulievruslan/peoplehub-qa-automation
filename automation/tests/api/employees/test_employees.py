from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.employees import Employees
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.generators.randoms import get_random_string, get_random_email, get_random_phone
from automation.dto.schema.employees_models import EmployeeStatus
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.constants import FIRST_NAME_RANDOM


@story("Employees")
@mark.employees
class TestEmployees(PeopleHubApi):

    @qase.id(id=60)
    @title("Get employees list")
    def test_get_employees_list(self):
        response = Employees(user=ADMIN).get_employees()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=61)
    @title("Create employee with valid data")
    def test_create_employee(
        self,
        create_employee_first_name: Fixture[str],
        get_random_department_id: Fixture[int],
        delete_employee_after_test: Fixture[None]
    ):
        response = Employees(user=ADMIN).post_employee(
            first_name=create_employee_first_name,
            last_name=f"last_name_by_AT {get_random_string()}",
            email=get_random_email(),
            position=f"Position_by_AT {get_random_string()}",
            department_id=get_random_department_id,
            phone=get_random_phone(),
            status=EmployeeStatus.ACTIVE,
        )

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()

    @qase.id(id=62)
    @title("Get employee by ID")
    def test_get_employee_by_id(self, create_employee_and_delete: Fixture[int]):
        response = Employees(user=ADMIN).get_employee_by_id(employee_id=create_employee_and_delete)

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=147)
    @title("Delete employee")
    @mark.parametrize("create_employee_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_employee(self, create_employee_and_delete: Fixture[int]):
        response = Employees(user=ADMIN).delete_employee(employee_id=create_employee_and_delete)

        response.assert_status_code(expected_code=204)

    @qase.id(id=149)
    @title("Update employee")
    def test_update_employee(
        self,
        get_random_department_id: Fixture[int],
        create_employee_and_delete: Fixture[int]
    ):
        response = Employees(user=ADMIN).update_employee(
            first_name=FIRST_NAME_RANDOM.format(random_string=get_random_string()),
            last_name=f"updated_last_name_by_AT {get_random_string()}",
            email=get_random_email(),
            position=f"Updated position_by_AT {get_random_string()}",
            employee_id=create_employee_and_delete,
            department_id=get_random_department_id,
            phone=get_random_phone(),
            status=EmployeeStatus.ON_LEAVE,
        )

        response.assert_status_code()
        response.assert_model_valid()
