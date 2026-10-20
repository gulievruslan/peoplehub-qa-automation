"""Module contains locators for the PeopleHub "Employees" page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class EmployeesPageLocatorsPW:
    """Locators for elements on "Employees" page."""
    TITLE_EMPLOYEES = LocatorPW(name="Title 'Employees'.", selector="//h1[text()='Employees']")
    TITLE_MANAGE_EMPLOYEES = LocatorPW(
        name="Title: 'Manage people across your organization'}",
        selector="//p[text()='Manage people across your organization']"
    )
    BUTTON_ADD_EMPLOYEE = LocatorPW(
        name="Add Employee button", selector="//*[@class='primary-button' and text()='+ Add Employee']"
    )
    TEXT_NAME_SURNAME = LocatorPW(
        name="Name and surname: {name_surname}", selector="//strong[normalize-space()='{name_surname}']"
    )
    TABLE_EMPLOYEES = LocatorPW(name="Employees table", selector="//table[@class='employees-table']")
    TEXT_EMAIL = LocatorPW(name="Email: {email}", selector="//span[text()='{email}']")
    TEXT_POSITION = LocatorPW(name="Position: {position}", selector="//td[text()='{position}']")
    TEXT_STATUS = TEXT_NAME_SURNAME.child(
        name="Status: {status}", selector="/following::*[@class='status-badge status-{status}']"
    )
    TEXT_DEPARTMENT = LocatorPW(name="Department {department}", selector="//td[text()='{department}']")
    FIELD_INPUT_SEARCH_EMPLOYEES = LocatorPW(
        name='Field input employees', selector='//input[@placeholder="Search employees..."]'
    )
    DROPDOWN_ALL_STATUSES = LocatorPW(name="Dropdown 'All statuses'", selector='//*[@class="employees-status-filter"]')
    OPTION_STATUS = LocatorPW(name="Option status {status}", selector='//option[@value="{status}"]')
    TEXT_EMPLOYEE_COUNT = LocatorPW(
        name="Employee count {count}", selector="//span[normalize-space()='{count} employee']"
    )
