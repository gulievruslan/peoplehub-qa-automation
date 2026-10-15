from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.notifications import Notifications
from automation.config.users import ADMIN
from automation.tests.allure_constants import PeopleHubApi


@story('Notifications')
@mark.notifications
class TestNotifications(PeopleHubApi):

    @qase.id(id=66)
    @title("Get notifications list")
    def test_get_notifications_list(self):
        response = Notifications(user=ADMIN).get_notifications()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=67)
    @title("Get unread notifications count")
    def test_get_unread_notifications_count(self):
        response = Notifications(user=ADMIN).get_unread_count()

        response.assert_status_code()
        response.assert_model_valid()
