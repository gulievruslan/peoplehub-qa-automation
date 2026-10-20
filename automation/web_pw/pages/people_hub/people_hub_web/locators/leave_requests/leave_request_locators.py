"""Module contains locators for the PeopleHub Leave Requests page."""
from playwright.sync_api import Page

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


def get_button_count(name: str, count: int) -> LocatorPW:
    """Create a locator for a button's count.

    Args:
        name: Button name
        count: Button count
    """
    return LocatorPW(
        name=f"{name} button count",
        locator_fn=lambda page: _get_button(name).get_locator(page).get_by_text(str(count), exact=True),
    )


def _get_column_header(name: str) -> LocatorPW:
    """Create a column header locator.

    Args:
        name: Name of the column header.
    """
    return LocatorPW(
        name=f"{name} column header",
        locator_fn=lambda page: page.get_by_role("columnheader", name=name),
    )


def get_leave_request_action_button(page: Page, name_surname: str, action: str) -> LocatorPW:
    """Create a locator for a leave request action button.

    Args:
        page: Playwright page instance.
        name_surname: Full name of the employee.
        action: Name of the action button.

    Returns:
        LocatorPW: Locator for the specified action button.
    """
    return LocatorPW(
        name=f"{action} button for {name_surname}",
        locator_fn=lambda page: page.get_by_role("row")
        .filter(has=page.get_by_text(name_surname, exact=True))
        .get_by_role("button", name=action),
        page=page,
    )


class LeaveRequestsPageLocatorsPW:
    """Locators for the PeopleHub Leave Requests page."""

    # Buttons
    new_request_button = _get_button(name="+ New Request")
    total_requests_button = _get_button(name="Total Requests")
    pending_button = _get_button(name="Pending")
    approved_button = _get_button(name="Approved")
    rejected_button = _get_button(name="Rejected")
    refresh_button = _get_button(name="Refresh")

    # Column Headers
    column_employee_header = _get_column_header(name='Employee')
    column_leave_period_header = _get_column_header(name='Leave Period')
    column_reason_header = _get_column_header(name='Reason')
    column_duration_header = _get_column_header(name='Duration')
    column_status_header = _get_column_header(name='Status')
    column_actions_header = _get_column_header(name='Actions')

    # Employee data
    employee_name_surname_field = LocatorPW(
        name="Employee name and surname {name_surname}",
        locator_fn=lambda page, name_surname: page.get_by_text(name_surname),
    )
    employee_leave_request_start_date = LocatorPW(
        name="Employee leave requests start date: {start_date}",
        locator_fn=lambda page, start_date: page.get_by_text(start_date),
    )
    employee_leave_request_end_date = LocatorPW(
        name="Employee leave requests end date: {end_date}",
        locator_fn=lambda page, end_date: page.get_by_text(end_date),
    )
    employee_leave_request_status = LocatorPW(
        name="Employee leave requests status: {status}",
        locator_fn=lambda page, status: page.get_by_role("table").get_by_text(status),
    )
    employee_leave_request_days = LocatorPW(
        name="Employee leave requests days",
        locator_fn=lambda page: page.get_by_role("cell", name="days"),
    )
    employee_leave_request_reason = LocatorPW(
        name="Employee leave requests reason: {reason}",
        locator_fn=lambda page, reason: page.get_by_text(reason),
    )

    leave_requests_title = LocatorPW(
        name="Leave Requests title",
        locator_fn=lambda page: page.get_by_role("heading", name="Leave Requests"),
    )
    page_description = LocatorPW(
        name="Leave Requests page description",
        locator_fn=lambda page: page.get_by_text("Review and manage employee"),
    )
    search_field = LocatorPW(
        name="Search leave requests field",
        locator_fn=lambda page: page.get_by_role("searchbox", name="Search leave requests"),
    )
    status_filter = LocatorPW(
        name="Filter by status",
        locator_fn=lambda page: page.get_by_label("Filter by status"),
    )
    message_leave_request_approved = LocatorPW(
        name="Message Leave Request marked as approved",
        locator_fn=lambda page, leave_request_id: page.locator(".leave-success").get_by_text(
            f"Request #{leave_request_id} marked as approved.", exact=True,
        ),
    )
    message_leave_request_deleted = LocatorPW(
        name="Message Leave Request deleted successfully",
        locator_fn=lambda page: page.locator(".leave-success").get_by_text(
            "Leave request deleted successfully.", exact=True,
        ),
    )
    message_leave_request_rejected = LocatorPW(
        name="Message Leave Request rejected successfully",
        locator_fn=lambda page, leave_request_id: page.locator(".leave-success").get_by_text(
            f"Request #{leave_request_id} marked as rejected.", exact=True,
        ),
    )
    message_leave_request_canceled = LocatorPW(
        name="Message Leave Request deleted successfully",
        locator_fn=lambda page: page.locator(".leave-success").get_by_text(
            "Leave request cancelled successfully.", exact=True,
        ),
    )
