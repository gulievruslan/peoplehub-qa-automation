from allure import story
from pytest import mark

from automation.api.auth import AuthClient
from automation.config.users import EMPLOYEE
from automation.custom.generators.randoms import get_random_email, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import NegativeAuth


@story('Authentification')
@mark.authentification
class TestAuthUser(PeopleHubApi):

    @mark.critical
    @typed_qase_id(qase_id=1)
    @typed_title(value="Login with valid credentials")
    def test_user_auth(self):
        response = AuthClient().login(email=EMPLOYEE.email, password=EMPLOYEE.password.get_secret_value())

        response.assert_status_code()
        response.assert_model_valid()

    @mark.critical
    @mark.negative
    @typed_qase_id(qase_id=2)
    @typed_title(value="Login with an incorrect password")
    def test_user_auth_wrong_password(self):
        response = AuthClient().login(email=EMPLOYEE.email, password=get_random_string())

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)

    @mark.critical
    @mark.negative
    @typed_qase_id(qase_id=3)
    @typed_title(value="Login with an unregistered email")
    def test_user_auth_wrong_email(self):
        response = AuthClient().login(email=get_random_email(), password=get_random_string())

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)

    @mark.negative
    @typed_qase_id(qase_id=4)
    @typed_title(value="Login with an invalid email format")
    def test_user_auth_wrong_email_format(self):
        response = AuthClient().login(email="test.com", password=get_random_string())

        response.assert_status_code(expected_code=422)
        response.assert_model_valid(is_error_model=True)

        detail = response.dto(is_error_model=True).detail[0]
        assert not isinstance(detail, str)
        assert detail.msg == NegativeAuth.NOT_VALID_EMAIL_ADDRESS

    @mark.negative
    @typed_qase_id(qase_id=5)
    @typed_title(value="Login without a required field")
    def test_user_auth_without_required_field(self):
        response = AuthClient().login(email=EMPLOYEE.email)

        response.assert_status_code(expected_code=422)
        response.assert_model_valid(is_error_model=True)

        detail = response.dto(is_error_model=True).detail[0]
        assert not isinstance(detail, str)
        assert detail.msg == NegativeAuth.VALID_STRING_INPUT
