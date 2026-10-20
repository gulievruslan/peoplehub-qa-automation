""""Module contains page object for the PeopleHub "Edit Leave Request". modal"""

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.people_hub_web.locators.leave_requests.edit_leave_request_modal_locators import (
    EditLeaveRequestsModalLocatorsPW,
)
from automation.web_pw.pages.people_hub.people_hub_web.modals.new_leave_request import LeaveRequestModal


class EditLeaveRequestModal(LeaveRequestModal, EditLeaveRequestsModalLocatorsPW):
    """Page Object for the PeopleHub edit leave request modal."""

    @step('Click button "Save changes"')
    def click_save_changes(self):
        """Click on the 'Save changes' button."""
        self.click_on_element(selector=self.button_save_changes)

    @step('Check leave request changed successfully')
    def check_leave_request_changed_successfully(self):
        """Check leave request changed successfully"""
        self.check_visibility(locator=self.message_leave_request_updated_success)
