from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.departments import Departments
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.tests.allure_constants import PeopleHubApi


@story('Departments')
@mark.deparments
class TestDepartments(PeopleHubApi):

    @qase.id(id=57)
    @title("Get departments list")
    def test_get_department_list(self):
        response = Departments(user=ADMIN).get_departments()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=58)
    @title("Create department with valid name")
    def test_create_department(self, create_random_department_name: Fixture[str], delete_department: Fixture[None]):
        response = Departments(user=ADMIN).post_department(name=create_random_department_name)

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()

    @qase.id(id=59)
    @title("Get department by ID")
    def test_get_department_by_id(self, create_department_and_delete: Fixture[int]):
        response = Departments(user=ADMIN).get_department_by_id(
            department_id=create_department_and_delete
        )

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=148)
    @title("Delete department")
    @mark.parametrize("create_department_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_department(self, create_department_and_delete: Fixture[int]):
        response = Departments(user=ADMIN).delete_department(
            department_id=create_department_and_delete
        )

        response.assert_status_code(expected_code=204)

    @qase.id(id=150)
    @title('Update department')
    def test_update_department(
        self, create_random_department_name: Fixture[str], create_department_and_delete: Fixture[int]
    ):
        response = Departments(user=ADMIN).update_department(
            department_id=create_department_and_delete, department_name=create_random_department_name
        )

        response.assert_status_code()
        response.assert_model_valid()
