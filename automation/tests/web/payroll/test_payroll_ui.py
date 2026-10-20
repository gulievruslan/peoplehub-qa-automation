from allure import story
from pytest import mark

from automation.config.users import ADMIN, EMPLOYEE, HR
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.dto.schema.payroll_models import PayrollListResponse
from automation.tests.allure_constants import PeopleHubWeb
from automation.tests.helper_functions import get_payroll_items_info
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


@story('Payroll')
@mark.payroll_ui
class TestPayrollUI(PeopleHubWeb):

    @typed_qase_id(qase_id=173)
    @typed_title(value='Display of the Payroll Completion card for HR Manager')
    @mark.parametrize("pw_open_page", [(HR, DashboardPage)], indirect=True)
    def test_payroll_completion(self, pw_open_page: Fixture[DashboardPage]):
        pw_open_page.check_payroll_completion_progress_bar_displaying()

    @typed_qase_id(qase_id=174)
    @typed_title(value='Display of Payroll Overview for HR Manager')
    @mark.parametrize("pw_open_page", [(HR, DashboardPage)], indirect=True)
    def test_payroll_overview(
        self,
        get_payroll_history: Fixture[dict[str, float | int]],
        pw_open_page: Fixture[DashboardPage]
    ):
        pw_open_page.check_employee_payment_displaying(employment_data=get_payroll_history)

    @typed_qase_id(qase_id=175)
    @typed_title(value='Display employee salaries in Salary by Employee')
    @mark.parametrize("pw_open_page", [(ADMIN, DashboardPage)], indirect=True)
    def test_employee_salaries(
        self,
        get_payroll_data_by_employee: Fixture[dict[str, int | float]],
        pw_open_page: Fixture[DashboardPage]
    ):
        pw_open_page.check_employee_salary_displaying(employee_data=get_payroll_data_by_employee)

    @typed_qase_id(qase_id=176)
    @typed_title(value='Display personal Payroll metrics for Employee')
    @mark.parametrize("pw_open_page", [(EMPLOYEE, DashboardPage)], indirect=True)
    def test_personal_payroll_metrics(
        self, get_all_payroll_data: Fixture[PayrollListResponse], pw_open_page: Fixture[DashboardPage]
    ):
        pw_open_page.check_employee_salary_statistics_displaying(
            latest_salary=get_all_payroll_data.items[0].salary,
            paid_amount=get_all_payroll_data.total_paid,
            records_count=get_all_payroll_data.total,
        )

    @typed_qase_id(qase_id=177)
    @typed_title(value='Display payroll history in My Payroll for Employee')
    @mark.parametrize("pw_open_page", [(EMPLOYEE, DashboardPage)], indirect=True)
    def test_payroll_history(
        self, get_all_payroll_data: Fixture[PayrollListResponse], pw_open_page: Fixture[DashboardPage]
    ):
        pw_open_page.check_payroll_items_displaying(payroll=get_payroll_items_info(get_all_payroll_data))
