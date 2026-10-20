"""Module contains page object for the PeopleHub login."""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.constants import TIME_ACTION
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.auth_page_locators import AuthPageLocatorsPW


class LoginPage(BasePeopleHubPage, AuthPageLocatorsPW):
    """Page Object for the PeopleHub login."""

    def __init__(self, page: Page):
        """Initialize the page.

        Args:
            page: Page Object for the PeopleHub login.
        """
        super().__init__(page=page, url="login")

    @step('Click on the "{field_name}" field')
    def click_on_field(self, field_name: str):
        """Click on a login form field.

        Args:
            field_name: Field name.
        """
        self.click_on_element(
            selector=self.FIELD_ENTER_DYNAMIC.format(field_name=field_name),
            description=f"{field_name.capitalize()} field",
        )

    @step('Enter value into the "{field_name}" field')
    def enter_field(self, field_name: str, value: str):
        """Enter a value into a login form field.

        Args:
            field_name: Field name.
            value: Value to enter into the field.
        """
        self.clear_and_type_like_user(
            locator=self.FIELD_ENTER_DYNAMIC.format(field_name=field_name),
            value=value,
        )

    @step('Check "sign in" button displaying')
    def check_sign_in_button_displaying(self):
        """Check "sign in" button displaying."""
        self.expect(target=self.BUTTON_SIGN_IN).to_be_visible(timeout=TIME_ACTION)


