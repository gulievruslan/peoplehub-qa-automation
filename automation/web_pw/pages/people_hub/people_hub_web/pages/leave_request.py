"""Module contains page object for the PeopleHub "Leave Request". page"""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.custom.generators.custom_date_time import CustomDateTime
from automation.dto.schema.leave_requests_models import LeaveRequestStatus
from automation.tests.web.enums import LeaveRequestActionButtonNames
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.leave_requests.leave_request_locators import (
    LeaveRequestsPageLocatorsPW,
    get_button_count,
    get_leave_request_action_button,
)


class LeaveRequestsPage(BasePeopleHubPage, LeaveRequestsPageLocatorsPW):
    """Page Object for the PeopleHub leave request."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub leave request.

        Args:
            page: Page Object for the PeopleHub leave request
        """
        super().__init__(page=page, url="leave-requests")

    @step('Check leave requests page content')
    def check_leave_requests_page_content(self):
        """Check leave requests page content"""
        self.soft_check_elements_visibility(
            locators=[
                self.new_request_button,
                self.total_requests_button,
                self.pending_button,
                self.approved_button,
                self.rejected_button,
                self.leave_requests_title,
                self.page_description,
                self.search_field,
                self.status_filter,
                self.refresh_button
            ]
        )

    @step('Click on search field')
    def click_on_search_field(self):
        """Click on search field"""
        self.click_on_element(selector=self.search_field)

    @step('Fill in name and surname: {name_surname}')
    def fill_in_name_surname_in_search_field(self, name_surname: str):
        """Click on search field

        Args:
            name_surname: Name and surname of employee to search for
        """
        self.clear_and_type_like_user(locator=self.search_field, value=name_surname)

    @step('Check employee data after search')
    def check_employee_data_after_search(
        self, name_surname: str, start_date: str, end_date: str, status: str, reason: str | None = None
    ):
        """Check employee data after search

        Args:
            name_surname: Name and surname of employee to search for
            start_date: leave request start date
            end_date: leave request end date
            reason: leave request reason
            status: employee leave request status
        """
        start_date = CustomDateTime(dt=(start_date, "%Y-%m-%dT%H:%M:%S.%f"), fmt="%b %d, %Y").as_string()
        end_date = CustomDateTime(dt=(end_date, "%Y-%m-%dT%H:%M:%S.%f"), fmt="%b %d, %Y").as_string()

        self.soft_check_elements_visibility(
            locators=[
                self.employee_name_surname_field.format(name_surname=name_surname),
                self.employee_leave_request_start_date.format(start_date=start_date),
                self.employee_leave_request_end_date.format(end_date=end_date),
                self.employee_leave_request_reason.format(reason=reason),
                self.employee_leave_request_days,
                self.employee_leave_request_status.format(status=status),
            ]
        )

    @step('Check leave requests statuses count')
    def check_leave_request_statuses_count(
        self, total_requests: int, pending_status_count:int, approved_status_count: int, rejected_status_count: int
    ):
        """Check leave requests statuses count

        Args:
            total_requests: Total Requests count
            pending_status_count: Pending status count
            approved_status_count: Approved status count
            rejected_status_count: Rejected status count
        """
        self.soft_check_elements_visibility(
            locators=[
                get_button_count(name="Total Requests", count=total_requests),
                get_button_count(name=LeaveRequestStatus.PENDING, count=pending_status_count),
                get_button_count(name=LeaveRequestStatus.APPROVED, count=approved_status_count),
                get_button_count(name=LeaveRequestStatus.REJECTED, count=rejected_status_count),
            ]
        )

    @step('Click button "+ New Request".')
    def click_button_new_request(self):
        """Click button "+ New Request"."""
        self.click_on_element(selector=self.new_request_button)

    @step('Click on button "{button}" leave request of employee "{name_surname}".')
    def click_on_request_action_button(self, name_surname: str, action_button: LeaveRequestActionButtonNames):
        """Click on button leave request of employee.

        Args:
            name_surname: Name and surname of employee to edit request
            action_button: action button name
        """
        self.click_on_element(
            get_leave_request_action_button(page=self.page, name_surname=name_surname, action=action_button)
        )

    @step('Check leave request with id: {leave_request_id} approved successfully')
    def check_leave_request_approved_successfully(self, leave_request_id: int):
        """Check leave request approved successfully

        Args:
            leave_request_id: leave_request id
        """
        self.check_visibility(
            locator=self.message_leave_request_approved.format(leave_request_id=leave_request_id),
        )

    @step('Check leave request with id: {leave_request_id} rejected')
    def check_leave_request_rejected(self, leave_request_id: int):
        """Check leave request rejected

        Args:
            leave_request_id: leave_request id
        """
        self.check_visibility(
            locator=self.message_leave_request_rejected.format(leave_request_id=leave_request_id),
        )
    @step('Check leave request canceled')
    def check_leave_request_canceled(self):
        """Check leave request canceled"""
        self.check_visibility(locator=self.message_leave_request_canceled)

    @step('Check leave request deleted')
    def check_leave_request_deleted(self):
        """Check leave request deleted"""
        self.check_visibility(locator=self.message_leave_request_deleted)

    @step('Confirm alert leave request')
    def confirm_alert_leave_request(
        self,
        name_surname: str,
        action_button: LeaveRequestActionButtonNames,
        accept: bool = True
    ):
        """Delete a department and handle the confirmation dialog.

        Args:
            name_surname: name and surname of employee cancelling request
            action_button: action button name
            accept: accept flag
        """
        self.handle_alert(
            action=lambda: self.click_on_element(
                selector=get_leave_request_action_button(
                    page=self.page, name_surname=name_surname, action=action_button
                )
            ),
            accept=accept,
        )