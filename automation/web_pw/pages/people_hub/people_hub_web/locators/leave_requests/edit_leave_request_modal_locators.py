"""Module contains locators for the PeopleHub "Edit Leave Requests" modal."""

from automation.web_playwright_custom.pages.base_pw.locators import LocatorPW


class EditLeaveRequestsModalLocatorsPW:
    """Locators for the PeopleHub "Edit Leave Requests" modal"""

    edit_leave_requests_title = LocatorPW(
        name="Edit Leave Request title",
        locator_fn=lambda page: page.get_by_role("heading", name="Edit Leave Request"),
    )
    edit_modal_description = LocatorPW(
        name="Edit Leave Request modal description",
        locator_fn=lambda page: page.get_by_text("Update the dates or reason"),
    )
    button_save_changes = LocatorPW(
        name="Button 'Save Changes'.",
        locator_fn=lambda page: page.get_by_role("button", name="Save Changes"),
    )
    button_close_form = LocatorPW(
        name="Button 'Close Form'.",
        locator_fn=lambda page: page.get_by_role("button", name="Close Form"),
    )
    message_leave_request_updated_success = LocatorPW(
        name="Message Leave Request updated successfully",
        locator_fn=lambda page: page.locator(".leave-success").get_by_text(
            "Leave request updated successfully.", exact=True,
        ),
    )
