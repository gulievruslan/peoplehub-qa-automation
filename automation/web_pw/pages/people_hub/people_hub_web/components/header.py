"""Module contains page object for the PeopleHub header component."""
from automation.custom.allure.custom_allure import step
from automation.web_pw.pages.people_hub.people_hub_web.locators.header_locators_pw import HeaderLocatorsPW
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


class HeaderComponent(DashboardPage, HeaderLocatorsPW):
    """Page Object for the PeopleHub header component."""

    @step('Click on button logout')
    def click_on_button_logout(self):
        """Click on button logout"""
        self.click_on_element(selector=self.BUTTON_LOGOUT, description=f"{self.BUTTON_LOGOUT.name} button")


