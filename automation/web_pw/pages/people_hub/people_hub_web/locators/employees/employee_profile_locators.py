"""Module contains locators for the PeopleHub "Employee Profile" page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class EmployeeProfilePageLocatorsPW:
    """Locators for elements on "Employee Profile" page."""
    TITLE_NAME_SURNAME = LocatorPW(
        name="Name and surname: {name_surname}", selector="//h1[normalize-space()='{name_surname}']"
    )
    TEXT_POSITION = LocatorPW(name='Positon text {position}', selector='//p[text()="{position}"]')
    TEXT_EMPLOYEE_CONTENT_DYNAMIC = LocatorPW(
        name="{field}: {field_value}",
        selector="//span[text()='{field}']/following::*[text()='{field_value}']"
    )
    CARD_EMPLOYEE_PROFILE = LocatorPW(name='Employee profile card', selector="//*[@class='employee-profile-card']")
    TEXT_EMPLOYEE_DEPARTMENT = CARD_EMPLOYEE_PROFILE.child(
        name='Department {department_name}',
        selector="/descendant::span[text()='Department']/following-sibling::*[text()='{department_name}']"
    )