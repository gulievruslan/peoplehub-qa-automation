from allure import story, title
from pytest import mark
from qase.pytest import qase

from automation.api.leave_requests import LeaveRequests
from automation.config.users import ADMIN, EMPLOYEE
from automation.custom.custom_typing import Fixture
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.custom.generators.randoms import get_random_string, get_random_number
from automation.dto.schema.auth_models import UserResponse
from automation.dto.schema.leave_requests_models import LeaveRequestStatus
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import LeaveRequestStatuses
from automation.tests.constants import LEAVE_REQUEST_RANDOM


@story("Leave Requests")
@mark.leave_requests
class TestLeaveRequests(PeopleHubApi):

    @qase.id(id=63)
    @title("Get leave requests list")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_get_leave_requests_list(self, create_leave_request_and_delete: Fixture[int]):
        response = LeaveRequests(user=ADMIN).get_leave_requests()

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=64)
    @title("Create leave request")
    @mark.parametrize('get_my_information', [EMPLOYEE], indirect=True)
    def test_create_leave_request(
        self,
        create_employee_leave_request: Fixture[str],
        get_my_information: Fixture[UserResponse],
        delete_leave_request_after_test: Fixture[None],
    ):
        response = LeaveRequests(user=EMPLOYEE).post_leave_request(
            employee_id=get_my_information.employee_id,
            start_date=CustomDateTime().get_offset_string(),
            end_date=CustomDateTime().get_offset_string(days=get_random_number(end=30)),
            reason=create_employee_leave_request,
        )

        response.assert_status_code(expected_code=201)
        response.assert_model_valid()

        response_dto = response.dto()

        assert response_dto.status == LeaveRequestStatuses.PENDING
        assert response_dto.reason == create_employee_leave_request

    @qase.id(id=65)
    @title("Get leave request by ID")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_get_leave_request_by_id(self, create_leave_request_and_delete: Fixture[int]):
        response = LeaveRequests(user=ADMIN).get_leave_request_by_id(
            leave_request_id=create_leave_request_and_delete
        )

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=151)
    @title("Update leave request")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_update_leave_request(self, create_leave_request_and_delete: Fixture[int]):
        response = LeaveRequests(user=ADMIN).update_leave_request(
            leave_request_id=create_leave_request_and_delete,
            start_date=CustomDateTime().get_offset_string(),
            end_date=CustomDateTime().get_offset_string(days=get_random_number(end=30)),
            reason=f"Updated reason_by_AT {get_random_string()}",
            status=LeaveRequestStatus.REJECTED,
        )

        response.assert_status_code()
        response.assert_model_valid()

    @qase.id(id=152)
    @title("Delete leave request")
    @mark.parametrize("create_leave_request_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_leave_request(self, create_leave_request_and_delete: Fixture[int]):
        response = LeaveRequests(user=ADMIN).delete_leave_request(leave_request_id=create_leave_request_and_delete)

        response.assert_status_code(expected_code=204)
