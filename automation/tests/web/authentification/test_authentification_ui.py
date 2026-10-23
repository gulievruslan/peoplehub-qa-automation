from allure import story
from pytest import mark

from automation.config.users import EMPLOYEE
from automation.custom.custom_typing import Fixture
from automation.custom.generators.randoms import get_random_email, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.web_playwright_custom.pages.base_pw import LocatorPW
from automation.web_pw.pages.people_hub.constants import TIME_WAIT
from automation.web_pw.pages.people_hub.people_hub_web.components.header import HeaderComponent
from automation.web_pw.pages.people_hub.people_hub_web.components.sidebar import SidebarComponent
from automation.web_pw.pages.people_hub.people_hub_web.pages.dashboard_page import DashboardPage
from automation.web_pw.pages.people_hub.people_hub_web.pages.login_page import LoginPage


@story('Authentification')
@mark.authentification_ui
class TestAuthUserUI(PeopleHubWeb):

    @staticmethod
    def _verify_login_validation(page: LoginPage, email: str, password: str, expected_locator: LocatorPW):
        """Verify login validation

        Args:
            page: page instant
            email: user email
            password: user password
            expected_locator: expected locator
        """
        page.click_on_field(field_name="email")
        page.enter_field(field_name="email", value=email)
        page.click_on_field(field_name="password")
        page.enter_field(field_name="password", value=password)
        page.click_on_element(selector=page.BUTTON_SIGN_IN)
        page.expect(expected_locator).to_be_visible(timeout=TIME_WAIT)

    @typed_qase_id(qase_id=74)
    @typed_title(value="Login with invalid credentials")
    @mark.parametrize("pw_open_page", [(None, LoginPage, {"authenticated": False})], indirect=True)
    def test_login_with_invalid_credentials(self, pw_open_page: Fixture[LoginPage]):
        self._verify_login_validation(
            page=pw_open_page,
            email=get_random_email(),
            password=get_random_string(),
            expected_locator=LoginPage.TEXT_INVALID_CREDENTIALS,
        )

    @typed_qase_id(qase_id=75)
    @typed_title(value="Login form required-field validation")
    @mark.parametrize("pw_open_page", [(None, LoginPage, {"authenticated": False})], indirect=True)
    def test_login_form_required_field_validation(self, pw_open_page: Fixture[LoginPage]):
        self._verify_login_validation(
            page=pw_open_page,
            email="",
            password="",
            expected_locator=LoginPage.TEXT_MANDATORY_FIELDS_REQUIRED,
        )

    @typed_qase_id(qase_id=135)
    @typed_title(value='Login with valid credentials')
    @mark.parametrize("pw_open_page", [(None, LoginPage, {"authenticated": False})], indirect=True)
    def test_login_with_valid_credentials(self, pw_open_page: Fixture[LoginPage]):
        pw_open_page.click_on_field(field_name="email")
        pw_open_page.enter_field(field_name="email", value=EMPLOYEE.email)
        pw_open_page.click_on_field(field_name="password")
        pw_open_page.enter_field(field_name="password", value=EMPLOYEE.password.get_secret_value())
        pw_open_page.click_on_element(selector=pw_open_page.BUTTON_SIGN_IN)

        SidebarComponent(page=pw_open_page.page).check_success_login_via_logo()

    @typed_qase_id(qase_id=136)
    @typed_title(value="Logout from the application")
    @mark.parametrize("pw_open_page", [(EMPLOYEE, DashboardPage)], indirect=True)
    def test_logout_from_application(self, pw_open_page: Fixture[DashboardPage]):
        page = pw_open_page.page
        HeaderComponent(page=page).click_on_button_logout()
        LoginPage(page=page).check_sign_in_button_displaying()

        assert (
            page.evaluate("localStorage.getItem('access_token')") is None
        ), "Access token should be removed from localStorage after logout"
