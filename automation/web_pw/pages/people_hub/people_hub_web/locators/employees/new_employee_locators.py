"""Module contains locators for the PeopleHub new employees page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class NewEmployeesPageLocatorsPW:
    """Locators for the PeopleHub new employees page."""
    TITLE_ADD_EMPLOYEE = LocatorPW(
        name="Title 'Add Employee'.", selector="//h1[text()='Add Employee']"
    )
    TITLE_EMPLOYEE_INFORMATION = LocatorPW(
        name="Title 'Employee Information'.",
        selector="//h2[text()='Employee Information']"
    )
    TITLE_CREATE_NEW_EMPLOYEE = LocatorPW(
        name="Title: Create a new employee profile",
        selector="//p[text()='Create a new employee profile']",
    )
    BUTTON_CREATE_EMPLOYEE = LocatorPW(
        name="Button 'Create Employee'.",
        selector="//button[@class='primary-button' and text()='Create Employee']",
    )
    INPUT_FIELD_DYNAMIC = LocatorPW(name="Input field dynamic {field}.", selector="//*[@id='{field}']")
