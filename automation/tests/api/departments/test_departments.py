from allure import story
from pytest import mark

from automation.api.departments import Departments
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi


@story('Departments')
@mark.deparments
class TestDepartments(PeopleHubApi):

    @typed_qase_id(qase_id=57)
    @typed_title(value="Get departments list")
    def test_get_department_list(self):
        response = Departments(user=ADMIN).get_departments()

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=58)
    @typed_title(value="Create department with valid name")
    def test_create_department(self, create_random_department_name: Fixture[str], delete_department: Fixture[None]):
        response = Departments(user=ADMIN).post_department(name=create_random_department_name)

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()

    @typed_qase_id(qase_id=59)
    @typed_title(value="Get department by ID")
    def test_get_department_by_id(self, create_department_and_delete: Fixture[int]):
        response = Departments(user=ADMIN).get_department_by_id(
            department_id=create_department_and_delete
        )

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=148)
    @typed_title(value="Delete department")
    @mark.parametrize("create_department_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_department(self, create_department_and_delete: Fixture[int]):
        response = Departments(user=ADMIN).delete_department(
            department_id=create_department_and_delete
        )

        response.assert_status_code(expected_code=204)

    @typed_qase_id(qase_id=150)
    @typed_title(value='Update department')
    def test_update_department(
        self, create_random_department_name: Fixture[str], create_department_and_delete: Fixture[int]
    ):
        response = Departments(user=ADMIN).update_department(
            department_id=create_department_and_delete, department_name=create_random_department_name
        )

        response.assert_status_code()
        response.assert_model_valid()
