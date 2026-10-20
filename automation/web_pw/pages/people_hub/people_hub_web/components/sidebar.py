"""Module contains page object for the PeopleHub sidebar component."""
from automation.custom.allure_custom.custom_allure import step
from automation.tests.web.enums import SidebarMenuButtonNames
from automation.web_pw.pages.people_hub.constants import TIME_WAIT
from automation.web_pw.pages.people_hub.people_hub_web.locators.sidebar_locators import SidebarLocatorsPW
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage


class SidebarComponent(DashboardPage, SidebarLocatorsPW):
    """Page Object for the PeopleHub sidebar component."""

    @step("Verify successful login by sidebar logo")
    def check_success_login_via_logo(self):
        """Verify that the sidebar logo is visible after login."""
        self.expect(self.LOGO).to_be_visible(timeout=TIME_WAIT)


    @step('Click sidebar element')
    def click_sidebar_element(self, href_element: str, text: SidebarMenuButtonNames):
        """Click sidebar element.

        Args:
            href_element: href element
            text: side menu text
        """
        self.click_on_element(selector=self.ELEMENT_SIDEBAR_DYNAMIC.format(text=text))

    @step("Check sidebar elements displaying")
    def check_sidebar_elements_displaying(self):
        """Check that sidebar elements are displayed."""
        for sidebar_element in SidebarMenuButtonNames:
            self.soft_check_visibility(locator=self.ELEMENT_SIDEBAR_DYNAMIC.format(text=sidebar_element))

    @step('Check sidebar element is active')
    def check_sidebar_element_is_active(self, href_element: str, text: SidebarMenuButtonNames):
        """Check sidebar element is active.

        Args:
            href_element: href element
            text: side menu text
        """
        self.soft_check_visibility(
            locator=self.ELEMENT_SIDEBAR_ACTIVE_DYNAMIC.format(href_element=href_element, text=text)
        )