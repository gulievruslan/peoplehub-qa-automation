from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.employees import Employees
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import NegativeAuth


@story('Data access')
@mark.data_access
class TestDataAccess(PeopleHubApi):

    @qase.id(id=52)
    @title("Access protected endpoint without authentication")
    def test_access_protect(self):
        response = Employees().get_employees()

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)
        assert response.dto(is_error_model=True).detail == NegativeAuth.NOT_AUTHENTICATED
