from allure import story
from pytest import mark

from automation.config.users import ADMIN, EMPLOYEE, HR
from automation.custom.custom_typing import Fixture
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.custom.generators.randoms import get_random_number, get_random_string
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.tests.constants import LEAVE_REQUEST_REASON_RANDOM, M_D_Y_DATE
from automation.tests.custom_types import EmployeeParams, LeaveRequestParams, LeaveRequestStatusCounts
from automation.tests.web.enums import LeaveRequestActionButtonNames
from automation.web_pw.pages.people_hub.people_hub_web.modals.edit_leave_request import EditLeaveRequestModal
from automation.web_pw.pages.people_hub.people_hub_web.modals.new_leave_request import LeaveRequestModal
from automation.web_pw.pages.people_hub.people_hub_web.pages.leave_request import LeaveRequestsPage


@story('Leave Requests')
@mark.leave_requests_ui
class TestLeaveRequestsUI(PeopleHubWeb):

    @typed_qase_id(qase_id=154)
    @typed_title(value='Open Leave Requests page')
    @mark.parametrize("pw_open_page", [(ADMIN, LeaveRequestsPage)], indirect=True)
    def test_open_leave_requests_page(self, pw_open_page: Fixture[LeaveRequestsPage]):
        pw_open_page.check_leave_requests_page_content()

    @typed_qase_id(qase_id=155)
    @typed_title(value='Search leave requests')
    @mark.parametrize("pw_open_page", [(ADMIN, LeaveRequestsPage)], indirect=True)
    def test_search_leave_request(
        self,
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        name_surname = f'{create_leave_request_and_delete['first_name']} {create_leave_request_and_delete['last_name']}'
        pw_open_page.click_on_search_field()
        pw_open_page.fill_in_name_surname_in_search_field(name_surname=name_surname)

        pw_open_page.check_employee_data_after_search(
            name_surname=name_surname,
            start_date=create_leave_request_and_delete['start_date'],
            end_date=create_leave_request_and_delete['end_date'],
            reason=create_leave_request_and_delete['reason'],
            status=create_leave_request_and_delete['status']
        )

    @typed_qase_id(qase_id=156)
    @typed_title(value='Filter leave requests by status')
    @mark.parametrize("pw_open_page", [(ADMIN, LeaveRequestsPage)], indirect=True)
    def test_filter_leave_request_by_status(
        self,
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        get_leave_request_status_counts: Fixture[LeaveRequestStatusCounts],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        counts = get_leave_request_status_counts

        pending_count = counts["pending"]
        approved_count = counts["approved"]
        rejected_count = counts["rejected"]

        pw_open_page.check_leave_request_statuses_count(
            total_requests=pending_count + approved_count + rejected_count,
            pending_status_count=pending_count,
            approved_status_count=approved_count,
            rejected_status_count=rejected_count,
        )

    @typed_qase_id(qase_id=157)
    @typed_title(value='Create a leave request as HR')
    @mark.parametrize(
        "delete_leave_request_after_test, pw_open_page",
        [({'reason':LEAVE_REQUEST_REASON_RANDOM}, (HR, LeaveRequestModal))],
        indirect=True
    )
    def test_hr_create_leave_requests(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        delete_leave_request_after_test: Fixture[None],
        pw_open_page: Fixture[LeaveRequestModal]
    ):
        pw_open_page.click_button_new_request()
        pw_open_page.click_on_select_employee()
        pw_open_page.select_employee(
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}'
        )
        pw_open_page.fill_start_end_dates(
            start_date=CustomDateTime(fmt=M_D_Y_DATE).get_offset_string(to_the_future=False),
            end_date=CustomDateTime(fmt=M_D_Y_DATE).get_offset_string(days=get_random_number(end=14))
        )
        pw_open_page.fill_in_leave_request_reason(reason=LEAVE_REQUEST_REASON_RANDOM)
        pw_open_page.click_button_submit_request()

        pw_open_page.check_leave_request_created()

    @typed_qase_id(qase_id=158)
    @typed_title(value='Edit a pending leave request')
    @mark.parametrize("pw_open_page", [(ADMIN, EditLeaveRequestModal)], indirect=True)
    def test_edit_pending_leave_request(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[EditLeaveRequestModal]
    ):
        pw_open_page.click_on_request_action_button(
            action_button=LeaveRequestActionButtonNames.EDIT,
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}'
        )
        pw_open_page.click_on_field_reason()
        pw_open_page.fill_in_leave_request_reason(reason=f'Reason Created by AT and {get_random_string()}')
        pw_open_page.click_save_changes()

        pw_open_page.check_leave_request_changed_successfully()

    @typed_qase_id(qase_id=159)
    @typed_title(value='Approve a pending leave request')
    @mark.parametrize("pw_open_page", [(ADMIN, LeaveRequestsPage)], indirect=True)
    def test_approve_pending_leave_request(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        pw_open_page.click_on_request_action_button(
            action_button=LeaveRequestActionButtonNames.APPROVE,
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}'
        )

        pw_open_page.check_leave_request_approved_successfully(
            leave_request_id=create_leave_request_and_delete['leave_request_id']
        )

    @typed_qase_id(qase_id=160)
    @typed_title(value='Reject a pending leave request')
    @mark.parametrize("pw_open_page", [(ADMIN, LeaveRequestsPage)], indirect=True)
    def test_reject_pending_leave_request(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        pw_open_page.click_on_request_action_button(
            action_button=LeaveRequestActionButtonNames.REJECT,
            name_surname=f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}'
        )

        pw_open_page.check_leave_request_rejected(
            leave_request_id=create_leave_request_and_delete['leave_request_id']
        )

    @typed_qase_id(qase_id=161)
    @typed_title(value='Cancel own pending leave request')
    @mark.parametrize(
        "create_leave_request_and_delete, pw_open_page",
        [
            (
                    {'user': EMPLOYEE, 'need_teardown': False},
                    (EMPLOYEE, LeaveRequestsPage)
            )
        ],
        indirect=True
    )
    def test_cancel_own_pending_leave_request(
        self,
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        name_surname = 'My request'

        pw_open_page.click_on_request_action_button(
            name_surname=name_surname, action_button=LeaveRequestActionButtonNames.CANCEL,
        )
        pw_open_page.confirm_alert_leave_request(
            name_surname=name_surname, action_button=LeaveRequestActionButtonNames.CANCEL,
        )

        pw_open_page.check_leave_request_canceled()

    @typed_qase_id(qase_id=162)
    @typed_title(value='Delete a leave request as administrator')
    @mark.parametrize(
        "create_leave_request_and_delete, pw_open_page",
        [({'need_teardown': False}, (ADMIN, LeaveRequestsPage))],
        indirect=True
    )
    def test_admin_delete_leave_request(
        self,
        create_employee_and_delete: Fixture[EmployeeParams],
        create_leave_request_and_delete: Fixture[LeaveRequestParams],
        pw_open_page: Fixture[LeaveRequestsPage]
    ):
        name_surname = f'{create_employee_and_delete['first_name']} {create_employee_and_delete['last_name']}'

        pw_open_page.click_on_request_action_button(
            action_button=LeaveRequestActionButtonNames.DELETE, name_surname=name_surname
        )
        pw_open_page.confirm_alert_leave_request(
            action_button=LeaveRequestActionButtonNames.DELETE, name_surname=name_surname
        )

        pw_open_page.check_leave_request_deleted()
