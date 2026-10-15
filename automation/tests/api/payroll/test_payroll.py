from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.payroll import Payroll
from automation.config.users import ADMIN, EMPLOYEE
from automation.custom.custom_typing import Fixture
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.custom.generators.randoms import get_random_number
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import PayrollStatuses


@story('Payroll')
@mark.payroll
class TestPayroll(PeopleHubApi):

    @qase.id(id=68)
    @title("Get payroll list")
    def test_get_payrolls_list(self):
        response = Payroll(user=EMPLOYEE).get_payroll()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=69)
    @title("Create payroll record")
    def test_create_payroll(
        self,
        create_employee_and_delete: Fixture[int],
        delete_payroll_after_test: Fixture[None]
    ):
        response = Payroll(user=ADMIN).post_payroll(
            employee_id=create_employee_and_delete,
            month=CustomDateTime().month,
            year=CustomDateTime().year,
            salary=get_random_number(end=4000)
        )

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()
        assert response.dto().status == PayrollStatuses.PENDING
