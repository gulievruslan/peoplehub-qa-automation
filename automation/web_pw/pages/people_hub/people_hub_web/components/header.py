"""Module contains page object for the PeopleHub header component."""
from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.constants import TIME_WAIT
from automation.web_pw.pages.people_hub.people_hub_web.locators.header_locators import HeaderLocatorsPW
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


class HeaderComponent(DashboardPage, HeaderLocatorsPW):
    """Page Object for the PeopleHub header component."""

    @step('Click on button logout')
    def click_on_button_logout(self):
        """Click on button logout"""
        self.click_on_element(selector=self.BUTTON_LOGOUT, description=f"{self.BUTTON_LOGOUT.name} button")


    @step('Check role information in header')
    def check_role_information_in_header(self, role: str):
        """Check role information in header

        Args:
            role (str): role name
        """
        self.expect(target=self.TEXT_ROLE_DYNAMIC.format(role=role)).to_be_visible(timeout=TIME_WAIT)


