"""Locators for the PeopleHub "Departments" page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class DepartmentsPageLocatorsPW:
    """Locators for elements on "Departments" page."""
    TITLE_DEPARTMENTS_DYNAMIC = LocatorPW(name="Dashboard title: 'Departments'.", selector="//h1[text()='Departments']")
    TEXT_TOOLTIP = LocatorPW(name="Tooltip text", selector="//p[text()='Manage departments across your organization']")
    BUTTON_PRIMARY_DEPARTMENT_DYNAMIC = LocatorPW(
        name="Button '{button}'", selector="//button[@class='primary-button' and text()='{button}']"
    )
    TOOLBAR_DEPARTMENTS = LocatorPW(name='Departments toolbar', selector="//*[@class='departments-toolbar']")
    TABLE_DEPARTMENTS = LocatorPW(name="Departments table", selector="//*[@class='departments-table-container']")
    TEXT_DEPARTMENT_NAME = LocatorPW(
        name="Department name: '{department_name}'.",
        selector="//*[@class='department-name']/strong[text()='{department_name}']"
    )
    BUTTON_EDIT_DEPARTMENT = LocatorPW(
        name="Edit department: '{department_name}' button",
        selector="//strong[text()='{department_name}']/following::*[@class='secondary-button' and text()='Edit'][1]"
    )
    BUTTON_DELETE_DEPARTMENT = LocatorPW(
        name="Delete department: '{department_name}' button",
        selector="//strong[text()='{department_name}']/following::*[@class='danger-button' and text()='Delete'][1]"
    )
    INPUT_FIELD_EDIT_DEPARTMENT = LocatorPW(
        name="Edit department: '{department_name}' field",
        selector="//*[@class='department-edit-input' and @value='{department_name}']"
    )
    TEXT_DEPARTMENT_WARNING_EMPTY = LocatorPW(
        name='Text warning: Department name cannot be empty.',
        selector="//*[@class='form-error' and text()='Department name cannot be empty.']"
    )
    FIELD_INPUT_SEARCH_DEPARTMENTS = LocatorPW(
        name='Field input department', selector='//input[@placeholder="Search departments..."]'
    )
