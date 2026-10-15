from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.auth import AuthClient
from automation.config.users import EMPLOYEE
from automation.custom.generators.randoms import get_random_email, get_random_string
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import NegativeAuth


@story('Authentification')
@mark.authentification
class TestAuthUser(PeopleHubApi):

    @qase.id(id=1)
    @mark.critical
    @title("Login with valid credentials")
    def test_user_auth(self):
        response = AuthClient().login(email=EMPLOYEE.email, password=EMPLOYEE.password.get_secret_value())

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=2)
    @mark.critical
    @mark.negative
    @title("Login with an incorrect password")
    def test_user_auth_wrong_password(self):
        response = AuthClient().login(email=EMPLOYEE.email, password=get_random_string())

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)

    @qase.id(id=3)
    @mark.critical
    @mark.negative
    @title("Login with an unregistered email")
    def test_user_auth_wrong_email(self):
        response = AuthClient().login(email=get_random_email(), password=get_random_string())

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)

    @qase.id(id=4)
    @mark.negative
    @title("Login with an invalid email format")
    def test_user_auth_wrong_email_format(self):
        response = AuthClient().login(email='test.com', password=get_random_string())

        response.assert_status_code(expected_code=422)
        response.assert_model_valid(is_error_model=True)

        assert response.dto(is_error_model=True).detail[0].msg == NegativeAuth.NOT_VALID_EMAIL_ADDRESS

    @qase.id(id=5)
    @mark.negative
    @title('Login without a required field')
    def test_user_auth_without_required_field(self):
        response = AuthClient().login(email=EMPLOYEE.email)

        response.assert_status_code(expected_code=422)
        response.assert_model_valid(is_error_model=True)
        assert response.dto(is_error_model=True).detail[0].msg == NegativeAuth.VALID_STRING_INPUT
