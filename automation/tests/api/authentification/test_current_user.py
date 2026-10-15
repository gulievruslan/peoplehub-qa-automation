from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.auth import AuthClient
from automation.config.users import EMPLOYEE
from automation.custom.custom_typing import Fixture
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import NegativeAuth


@story('Current user')
@mark.current_user
class TestCurrentUser(PeopleHubApi):

    @qase.id(id=6)
    @title("Get current user with a valid token")
    @mark.parametrize('get_user_token', [EMPLOYEE], indirect=True)
    def test_user_auth(self, get_user_token: Fixture[str]):
        response = AuthClient().get_me(access_token=get_user_token)

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=7)
    @mark.negative
    @title("Get current user without an access token")
    def test_user_auth_without_access_token(self):
        response = AuthClient().get_me()

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)
        assert response.dto(is_error_model=True).detail == NegativeAuth.NOT_AUTHENTICATED

    @qase.id(id=8)
    @mark.negative
    @title("Get current user with an invalid token")
    def test_user_auth_with_invalid_token(self):
        response = AuthClient().get_me(access_token='invalid_token')

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)
        assert response.dto(is_error_model=True).detail == NegativeAuth.INVALID_OR_EXPIRED_TOKEN
