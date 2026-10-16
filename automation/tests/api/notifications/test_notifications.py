from allure import story
from pytest import mark

from automation.api.notifications import Notifications
from automation.config.users import ADMIN
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubApi


@story('Notifications')
@mark.notifications
class TestNotifications(PeopleHubApi):

    @typed_qase_id(qase_id=66)
    @typed_title(value="Get notifications list")
    def test_get_notifications_list(self):
        response = Notifications(user=ADMIN).get_notifications()

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=67)
    @typed_title(value="Get unread notifications count")
    def test_get_unread_notifications_count(self):
        response = Notifications(user=ADMIN).get_unread_count()

        response.assert_status_code()
        response.assert_model_valid()
