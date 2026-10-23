from allure import story
from pytest import mark

from automation.api.leave_requests import LeaveRequests
from automation.config.users import ADMIN, EMPLOYEE
from automation.custom.custom_typing import Fixture
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.custom.generators.randoms import get_random_number, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.dto.schema.auth_models import UserResponse
from automation.dto.schema.leave_requests_models import LeaveRequestStatus
from automation.tests.allure_constants import PeopleHubApi
from automation.tests.api.enums import LeaveRequestStatuses
from automation.tests.constants import ASSERT_MESSAGE
from automation.tests.custom_types import LeaveRequestParams


@story("Leave Requests")
@mark.leave_requests
class TestLeaveRequests(PeopleHubApi):

    @typed_qase_id(qase_id=63)
    @typed_title(value="Get leave requests list")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_get_leave_requests_list(self, create_leave_request_and_delete: Fixture[int]):
        response = LeaveRequests(user=ADMIN).get_leave_requests()

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=64)
    @typed_title(value="Create leave request")
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

        assert (
            response_dto.status == LeaveRequestStatuses.PENDING
        ), ASSERT_MESSAGE.format(expected=LeaveRequestStatuses.PENDING, actual=response_dto.status)
        assert (
            response_dto.reason == create_employee_leave_request
        ), ASSERT_MESSAGE.format(expected=LeaveRequestStatuses.PENDING, actual=response_dto.reason)

    @typed_qase_id(qase_id=65)
    @typed_title(value="Get leave request by ID")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_get_leave_request_by_id(self, create_leave_request_and_delete: Fixture[LeaveRequestParams]):
        response = LeaveRequests(user=ADMIN).get_leave_request_by_id(
            leave_request_id=create_leave_request_and_delete['leave_request_id']
        )

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=151)
    @typed_title(value="Update leave request")
    @mark.parametrize("create_leave_request_and_delete", [{"reason": "Reason created by AT"}], indirect=True)
    def test_update_leave_request(self, create_leave_request_and_delete: Fixture[LeaveRequestParams]):
        response = LeaveRequests(user=ADMIN).update_leave_request(
            leave_request_id=create_leave_request_and_delete['leave_request_id'],
            start_date=CustomDateTime().get_offset_string(),
            end_date=CustomDateTime().get_offset_string(days=get_random_number(end=30)),
            reason=f"Updated reason_by_AT {get_random_string()}",
            status=LeaveRequestStatus.REJECTED,
        )

        response.assert_status_code()
        response.assert_model_valid()

    @typed_qase_id(qase_id=152)
    @typed_title(value="Delete leave request")
    @mark.parametrize("create_leave_request_and_delete", [{"need_teardown": False}], indirect=True)
    def test_delete_leave_request(self, create_leave_request_and_delete: Fixture[LeaveRequestParams]):
        response = LeaveRequests(user=ADMIN).delete_leave_request(
            leave_request_id=create_leave_request_and_delete['leave_request_id']
        )

        response.assert_status_code(expected_code=204)
