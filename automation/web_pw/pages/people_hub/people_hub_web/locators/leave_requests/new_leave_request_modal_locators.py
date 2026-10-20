"""Module contains locators for the PeopleHub "New Leave Requests" modal."""

from automation.web_playwright_custom.pages.base_pw.locators import LocatorPW


def _get_button(name: str) -> LocatorPW:
    """Create a button locator by its accessible name.

    Args:
        name: Name of the button.
    """
    return LocatorPW(
        name=f"{name} button",
        locator_fn=lambda page: page.get_by_role("button", name=name),
    )


class NewLeaveRequestsModalLocatorsPW:
    """Locators for the PeopleHub "New Leave Requests" modal"""

    new_request_button = _get_button("+ New Request")
    leave_requests_title = LocatorPW(
        name="New Leave Request title",
        locator_fn=lambda page: page.get_by_role("heading", name="New Leave Request"),
    )
    modal_description = LocatorPW(
        name="New Leave Request modal description",
        locator_fn=lambda page: page.get_by_text("Enter the details for the"),
    )
    dropdown_select_employee = LocatorPW(name="Dropdown select employee", selector="#leave-employee")
    employee_option = LocatorPW(
        name="Employee option {name_surname}",
        locator_fn=lambda page, name_surname: page.locator("#leave-employee").get_by_role(
            "option", name=name_surname
        ),
    )
    textbox_start_date = LocatorPW(
        name="Textbox start date",
        locator_fn=lambda page: page.get_by_role("textbox", name="Start date"),
    )
    textbox_end_date = LocatorPW(
        name="Textbox end date",
        locator_fn=lambda page: page.get_by_role("textbox", name="End date"),
    )
    textbox_reason = LocatorPW(
        name='Textbox reason text',
        locator_fn=lambda page: page.get_by_role("textbox", name="Reason"),
    )
    button_submit_request = LocatorPW(
        name="Button 'Submit Request'.",
        locator_fn=lambda page: page.get_by_role("button", name="Submit Request"),
    )
    button_cancel = LocatorPW(
        name="Button 'Cancel'.",
        locator_fn=lambda page: page.get_by_role("button", name="Cancel"),
    )
    button_close_form = LocatorPW(
        name="Button 'Close Form'.",
        locator_fn=lambda page: page.get_by_role("button", name="Close Form"),
    )
    message_leave_request_submitted = LocatorPW(
        name="Message Leave Request submitted successfully",
        locator_fn=lambda page: page.locator(".leave-success").get_by_text(
            "Leave request submitted successfully.", exact=True,
        ),
    )
