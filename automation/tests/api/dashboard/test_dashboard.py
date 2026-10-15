from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.dashboard import Dashboard
from automation.config.users import ADMIN, EMPLOYEE
from automation.tests.allure_constants import PeopleHubApi


@story('Dashboard')
@mark.dashboard
class TestDashboard(PeopleHubApi):

    @qase.id(id=70)
    @title("Get dashboard statistics")
    def test_access_protect(self):
        response = Dashboard(user=ADMIN).get_dashboard()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=146)
    @title("Get dashboard statistics for the current user")
    def test_get_dashboard_statistics(self):
        response = Dashboard(user=EMPLOYEE).get_dashboard_me()

        response.assert_status_code()
        response.assert_model_valid()
