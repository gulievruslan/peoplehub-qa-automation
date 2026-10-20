"""Module contains page object for the PeopleHub "New Leave Request". modal"""

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.people_hub_web.locators.leave_requests.new_leave_request_modal_locators import (
    NewLeaveRequestsModalLocatorsPW,
)
from automation.web_pw.pages.people_hub.people_hub_web.pages.leave_request import LeaveRequestsPage


class LeaveRequestModal(LeaveRequestsPage, NewLeaveRequestsModalLocatorsPW):
    """Page Object for the PeopleHub new leave request modal."""

    @step('Click on dropdown "select employee"')
    def click_on_select_employee(self):
        """Click on select employee."""
        self.click_on_element(selector=self.dropdown_select_employee)

    @step("Select employee {name_surname}")
    def select_employee(self, name_surname: str):
        """Select employee.

        Args:
            name_surname: Employee name and surname.
        """
        self.dropdown_select_employee.select_option(label=name_surname)

    @step('Fill in start date {start_date} and end date {end_date}')
    def fill_start_end_dates(self, start_date: str, end_date: str):
        """Fill in start date and end date

        Args:
            start_date: Start date
            end_date: End date
        """
        self.click_on_element(selector=self.textbox_start_date)
        self.clear_and_type_like_user(locator=self.textbox_start_date, value=start_date)
        self.click_on_element(selector=self.textbox_end_date)
        self.clear_and_type_like_user(locator=self.textbox_end_date, value=end_date)

    @step('Click on field reason')
    def click_on_field_reason(self):
        """Click on field reason"""
        self.click_on_element(selector=self.textbox_reason)

    @step('Fill in leave request reason: {reason}')
    def fill_in_leave_request_reason(self, reason: str):
        """Fill in leave request reason

        Args:
            reason: Leave request reason
        """
        self.clear_and_type_like_user(locator=self.textbox_reason, value=reason)

    @step('Click button "Submit Request"')
    def click_button_submit_request(self):
        """Click on submit request"""
        self.click_on_element(selector=self.button_submit_request)

    @step('Check leave request created successfully')
    def check_leave_request_created(self):
        """Check leave request created successfully"""
        self.check_visibility(locator=self.message_leave_request_submitted)
