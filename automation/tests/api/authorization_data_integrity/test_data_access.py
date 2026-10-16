from allure import story
from pytest import mark

from automation.api.employees import Employees
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import NegativeAuth


@story('Data access')
@mark.data_access
class TestDataAccess(PeopleHubApi):

    @typed_qase_id(qase_id=52)
    @typed_title(value="Access protected endpoint without authentication")
    def test_access_protect(self):
        response = Employees().get_employees()

        response.assert_status_code(expected_code=401)
        response.assert_model_valid(is_error_model=True)
        assert response.dto(is_error_model=True).detail == NegativeAuth.NOT_AUTHENTICATED
