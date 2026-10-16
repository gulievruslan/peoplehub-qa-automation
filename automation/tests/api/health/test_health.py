from allure import story
from pytest import mark

from automation.api.health import Health
from automation.config.users import ADMIN
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import AppStatuses


@story('Health')
@mark.health
class TestHealth(PeopleHubApi):

    @typed_qase_id(qase_id=71)
    @typed_title(value="Check application health")
    def test_check_app_health(self):
        response = Health(user=ADMIN).get_health()

        response.assert_status_code()
        response.assert_model_valid()
        assert response.dto().status == AppStatuses.OK

    @typed_qase_id(qase_id=72)
    @typed_title(value="Check database health")
    def test_check_db_health(self):
        response = Health(user=ADMIN).get_database_health()

        response.assert_status_code()
        response.assert_model_valid()
        assert response.dto().database == AppStatuses.OK
