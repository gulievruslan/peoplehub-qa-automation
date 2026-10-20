"""Module contains locators for the PeopleHub new department page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class NewDepartmentsPageLocatorsPW:
    """Locators for the PeopleHub new department page."""
    TITLE_ADD_DEPARTMENT = LocatorPW(name="Title 'Add Department'.", selector="//h1[text()='Add Department']")
    TITLE_DEPARTMENT_INFORMATION = LocatorPW(
        name="Title 'Department Information'.", selector="//h2[text()='Department Information']"
    )
    TITLE_CREATE_NEW_DEPARTMENT = LocatorPW(
        name="Title 'Create a new department'.", selector="//p[text()='Create a new department']"
    )
    BUTTON_CREATE_DEPARTMENT = LocatorPW(
        name="Add department button", selector="//button[@class='primary-button' and text()='Create Department']"
    )
    BUTTON_CANCEL = LocatorPW(
        name="Cancel button", selector="//button[@class='secondary-button' and text()='Cancel']"
    )
    INPUT_FIELD_DEPARTMENT = LocatorPW(name="Input field department", selector="//*[@id='name']")