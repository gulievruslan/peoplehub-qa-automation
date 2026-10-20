from allure import story
from pytest import mark

from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


@story('Dashboard')
@mark.dashboard_ui
class TestDashboardUI(PeopleHubWeb):

    @typed_qase_id(qase_id=137)
    @typed_title(value='Check dashboard titles displaying.')
    @mark.parametrize("pw_open_page", [(ADMIN, DashboardPage)], indirect=True)
    def test_dashboard_displaying(self, pw_open_page: Fixture[DashboardPage]):
        pw_open_page.check_titles_displaying()
        pw_open_page.check_cards_displaying()
