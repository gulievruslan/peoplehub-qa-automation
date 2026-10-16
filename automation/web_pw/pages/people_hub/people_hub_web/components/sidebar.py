"""Module contains page object for the PeopleHub sidebar component."""
from automation.custom.allure.custom_allure import step
from automation.web_pw.pages.people_hub.constants import TIME_WAIT
from automation.web_pw.pages.people_hub.people_hub_web.locators.sidebar_locators_pw import SidebarLocatorsPW
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


class SidebarComponent(DashboardPage, SidebarLocatorsPW):
    """Page Object for the PeopleHub sidebar component."""

    @step("Verify successful login by sidebar logo")
    def check_success_login_via_logo(self):
        """Verify that the sidebar logo is visible after login."""
        self.expect(self.LOGO).to_be_visible(timeout=TIME_WAIT)