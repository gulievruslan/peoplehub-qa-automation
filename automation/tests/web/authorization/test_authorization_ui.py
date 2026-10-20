from allure import story
from pytest import mark

from automation.config.users import ADMIN, EMPLOYEE, HR, TestUser
from automation.custom.config import Config
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.web_pw.pages.people_hub.people_hub_web.components.header import HeaderComponent
from automation.web_pw.pages.people_hub.people_hub_web.pages.login_page import LoginPage


@story('Authorization')
@mark.authorization_ui
class TestAuthorizationUI(PeopleHubWeb):

    @typed_qase_id(qase_id=87)
    @typed_title(value='Verify that a user without an authenticated session cannot access protected pages.')
    @mark.parametrize("pw_open_page", [(None, LoginPage, {"authenticated": False})], indirect=True)
    def test_verify_without_auth(self, pw_open_page: Fixture[LoginPage]):
        pw_open_page.get(url=f'{Config.base_url}/dashboard')
        pw_open_page.check_current_url(expected_url=f'{Config.base_url}/login')
        pw_open_page.get(url=f'{Config.base_url}/employees')
        pw_open_page.check_current_url(expected_url=f'{Config.base_url}/login')
        pw_open_page.get(url=f'{Config.base_url}/departments')
        pw_open_page.check_current_url(expected_url=f'{Config.base_url}/login')
        pw_open_page.check_sign_in_button_displaying()


    @typed_qase_id(qase_id=145)
    @typed_title(value='Verify role information in the application header')
    @mark.parametrize(
        'user, role',
        [(EMPLOYEE, 'employee'), (ADMIN, 'admin'), (HR, 'hr_manager')]
    )
    @mark.parametrize("pw_open_page", [(None, LoginPage, {"authenticated": False})], indirect=True)
    def test_verify_role_header(self, pw_open_page: Fixture[LoginPage], user: TestUser, role: str):
        pw_open_page.click_on_field(field_name="email")
        pw_open_page.enter_field(field_name="email", value=user.email)
        pw_open_page.click_on_field(field_name="password")
        pw_open_page.enter_field(field_name="password", value=user.password.get_secret_value())
        pw_open_page.click_on_element(selector=pw_open_page.BUTTON_SIGN_IN)
        HeaderComponent(page=pw_open_page.page).check_role_information_in_header(role=role)