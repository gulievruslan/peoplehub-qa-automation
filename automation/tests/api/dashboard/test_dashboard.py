from allure import story
from pytest import mark

from automation.api.dashboard import Dashboard
from automation.config.users import ADMIN, EMPLOYEE
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi


@story('Dashboard')
@mark.dashboard
class TestDashboard(PeopleHubApi):

    @typed_qase_id(qase_id=70)
    @typed_title(value="Get dashboard statistics")
    def test_access_protect(self):
        response = Dashboard(user=ADMIN).get_dashboard()

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=146)
    @typed_title(value="Get dashboard statistics for the current user")
    def test_get_dashboard_statistics(self):
        response = Dashboard(user=EMPLOYEE).get_dashboard_me()

        response.assert_status_code()
        response.assert_model_valid()
