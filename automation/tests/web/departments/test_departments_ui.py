from allure import story
from pytest import mark

from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.tests.custom_types import DepartmentParams
from automation.tests.constants import TESTING_DEPARTMENT
from automation.tests.web.enums import DepartmentsButtonNames
from automation.web_pw.pages.people_hub.people_hub_web.pages.deparments.departments_page import DepartmentsPage
from automation.web_pw.pages.people_hub.people_hub_web.pages.deparments.new_department_page import NewDepartmentPage


@story('Departments')
@mark.departments_ui
class TestDepartmentsUI(PeopleHubWeb):

    @typed_qase_id(qase_id=143)
    @typed_title(value='Open departments page')
    @mark.parametrize("pw_open_page", [(ADMIN, DepartmentsPage)], indirect=True)
    def test_open_departments_page(self, pw_open_page: Fixture[DepartmentsPage]):
        pw_open_page.check_page_content_displaying()

    @typed_qase_id(qase_id=144)
    @typed_title(value='Create department')
    @mark.parametrize("pw_open_page", [(ADMIN, DepartmentsPage)], indirect=True)
    def test_create_department(
        self,
        create_random_department_name: Fixture[str],
        pw_open_page: Fixture[DepartmentsPage],
        delete_department: Fixture[None]
    ):
        pw_open_page.click_button_dynamic(button=DepartmentsButtonNames.ADD_DEPARTMENT)
        new_department_page = NewDepartmentPage(page=pw_open_page.page)
        new_department_page.check_new_department_content_displaying()
        new_department_page.click_input_field()
        new_department_page.fill_new_department(department_name=create_random_department_name)
        new_department_page.click_button_add_department()
        pw_open_page.check_department_displaying(department_name=create_random_department_name)

    @typed_qase_id(qase_id=170)
    @typed_title(value='Update department name')
    @mark.parametrize("create_department_and_delete", [{'department_name': TESTING_DEPARTMENT}], indirect=True)
    @mark.parametrize("pw_open_page", [(ADMIN, DepartmentsPage)], indirect=True)
    def test_update_department_name(
        self,
        create_random_department_name: Fixture[str],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[DepartmentsPage],
    ):
        pw_open_page.click_button_edit_department(department_name=TESTING_DEPARTMENT)
        pw_open_page.edit_department(
            department_name=TESTING_DEPARTMENT,
            new_department_name="",
        )
        pw_open_page.edit_department(
            department_name="",
            new_department_name=create_random_department_name,
        )
        pw_open_page.click_button_dynamic(button=DepartmentsButtonNames.SAVE)
        pw_open_page.check_department_displaying(department_name=create_random_department_name)

    @typed_qase_id(qase_id=171)
    @typed_title(value='Delete department as admin')
    @mark.parametrize(
        "create_department_and_delete, pw_open_page",
        [({"need_teardown": False}, (ADMIN, DepartmentsPage))],
        indirect=True
    )
    def test_update_department_name(
        self,
        create_random_department_name: Fixture[str],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[DepartmentsPage],
    ):
        pw_open_page.delete_department(department_name=create_random_department_name)
        pw_open_page.check_department_absence(department_name=create_random_department_name)

    @typed_qase_id(qase_id=172)
    @typed_title(value='Prevent saving department with empty name')
    @mark.parametrize("pw_open_page", [(ADMIN, DepartmentsPage)], indirect=True)
    def test_prevent_saving_department_with_empty_name(
        self,
        create_random_department_name: Fixture[str],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[DepartmentsPage]
    ):
        pw_open_page.click_button_edit_department(department_name=create_random_department_name)
        pw_open_page.edit_department(
            department_name=create_random_department_name,
            new_department_name="",
        )
        pw_open_page.click_button_dynamic(button=DepartmentsButtonNames.SAVE)
        pw_open_page.check_department_can_not_be_empty()


    @typed_qase_id(qase_id=179)
    @typed_title(value='Filter departments by name')
    @mark.parametrize("pw_open_page", [(ADMIN, DepartmentsPage)], indirect=True)
    def test_filter_departments_by_name(
        self,
        create_random_department_name: Fixture[str],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[DepartmentsPage],
    ):
        pw_open_page.click_input_field_department()
        pw_open_page.search_for_department(department_name=create_random_department_name)
        pw_open_page.check_department_displaying(department_name=create_random_department_name)
