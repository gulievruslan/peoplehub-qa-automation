from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.health import Health
from automation.config.users import ADMIN
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import AppStatuses


@story('Health')
@mark.health
class TestHealth(PeopleHubApi):

    @qase.id(id=71)
    @title("Check application health")
    def test_check_app_health(self):
        response = Health(user=ADMIN).get_health()

        response.assert_status_code()
        response.assert_model_valid()
        assert response.dto().status == AppStatuses.OK

    @qase.id(id=72)
    @title("Check database health")
    def test_check_db_health(self):
        response = Health(user=ADMIN).get_database_health()

        response.assert_status_code()
        response.assert_model_valid()
        assert response.dto().database == AppStatuses.OK
