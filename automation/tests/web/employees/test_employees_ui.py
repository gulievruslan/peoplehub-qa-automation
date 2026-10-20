from allure import story
from pytest import mark

from automation.api.employees import Employees
from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.generators.randoms import get_random_email, get_random_phone, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.tests.custom_types import DepartmentParams, EmployeeParams
from automation.web_pw.pages.people_hub.people_hub_web.pages.employee.employee_profile_page import EmployeeProfilePage
from automation.web_pw.pages.people_hub.people_hub_web.pages.employee.employees_page import EmployeesPage
from automation.web_pw.pages.people_hub.people_hub_web.pages.employee.new_employee_page import NewEmployeesPage


@story('Employees')
@mark.employees_ui
class TestEmployeesUI(PeopleHubWeb):

    @typed_qase_id(qase_id=140)
    @typed_title(value='Open employees list')
    @mark.parametrize("pw_open_page", [(ADMIN, EmployeesPage)], indirect=True)
    def test_open_employees_list(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        pw_open_page: Fixture[EmployeesPage]
    ):
        pw_open_page.check_employee_content_displaying(
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}',
            email=f'{create_employee_and_delete["email"]}',
            position=f'{create_employee_and_delete["position"]}',
            department=f'{create_employee_and_delete["department_name"]}',
            status=f'{create_employee_and_delete["status"]}',
        )

    @typed_qase_id(qase_id=141)
    @typed_title(value='Create employee')
    @mark.parametrize("pw_open_page", [(ADMIN, EmployeesPage)], indirect=True)
    def test_create_employee(
        self,
        create_department_and_delete: Fixture[DepartmentParams],
        delete_employee_after_test: Fixture[None],
        create_employee_first_name: Fixture[str],
        pw_open_page: Fixture[EmployeesPage]
    ):
        pw_open_page.click_add_employee()

        new_employee_page = NewEmployeesPage(page=pw_open_page.page)

        last_name = f'last_name_random_{get_random_string()}'
        email = get_random_email()
        phone = get_random_phone()
        position = f'random_position_{get_random_string()}'
        department_id = str(create_department_and_delete['department_id'])

        new_employee_page.fill_employee_fields(
            first_name=create_employee_first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            position=position,
            department_id=department_id
        )
        new_employee_page.click_create_employee()

        response = Employees(user=ADMIN).get_employees()

        response.assert_status_code()
        response.assert_model_valid()

        employee_id = tuple(
            employee.id for employee in response.dto().root if employee.first_name == create_employee_first_name
        )

        EmployeeProfilePage(page=pw_open_page.page, employee_id=employee_id[0]).check_employee_profile(
            first_name=create_employee_first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            position=position,
            department_name=create_department_and_delete['department_name']
        )

    @typed_qase_id(qase_id=142)
    @typed_title(value='Open employee profile')
    @mark.parametrize("pw_open_page", [(ADMIN, EmployeesPage)], indirect=True)
    def test_open_employee_profile(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[EmployeesPage]
    ):
        employee_profile_page = EmployeeProfilePage(page=pw_open_page.page, employee_id=create_employee_and_delete['employee_id'])
        employee_profile_page.get()

        employee_profile_page.check_employee_profile(
            first_name=create_employee_and_delete['first_name'],
            last_name=create_employee_and_delete['last_name'],
            email=create_employee_and_delete['email'],
            phone=create_employee_and_delete['phone'],
            position=create_employee_and_delete['position'],
            department_name=create_department_and_delete['department_name']
        )

    @typed_qase_id(qase_id=180)
    @typed_title(value='Search and filter employees')
    @mark.parametrize("pw_open_page", [(ADMIN, EmployeesPage)], indirect=True)
    def test_filter_employees(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_department_and_delete: Fixture[DepartmentParams],
        pw_open_page: Fixture[EmployeesPage]
    ):
        pw_open_page.click_field_search_employees()
        pw_open_page.fill_employee_and_surname(name_surname=create_employee_and_delete['first_name'])

        pw_open_page.check_employee_data_displaying_after_searching(
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete["last_name"]}',
            email=create_employee_and_delete['email'],
            position=create_employee_and_delete['position'],
            department=create_department_and_delete['department_name'],
            status=create_employee_and_delete['status'],
        )
