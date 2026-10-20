"""Module contains page object for the PeopleHub new employees page."""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.employees.new_employee_locators import (
    NewEmployeesPageLocatorsPW,
)


class NewEmployeesPage(BasePeopleHubPage, NewEmployeesPageLocatorsPW):
    """Page Object for the PeopleHub new employee."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub new employee.

        Args:
            page: Page Object for the PeopleHub employees
        """
        super().__init__(page=page, url="employees/new")

    @step('Fill in employee data')
    def fill_employee_fields(
        self, first_name: str, last_name: str, email: str, phone: str, position: str, department_id: str
    ):
        """Fill in employee data fields.

        Args:
            first_name: First name of the employee
            last_name: Last name of the employee
            email: Email of the employee
            phone: Phone number of the employee
            position: Position of the employee
            department_id: Department ID of the employee
        """
        fields = ('first_name', 'last_name', 'email', 'phone', 'position', 'department_id')
        values = (first_name, last_name, email, phone, position, department_id)

        for field, value in zip(fields, values, strict=True):
            self.clear_and_type_like_user(locator=self.INPUT_FIELD_DYNAMIC.format(field=field), value=value)

    @step('Click button "Create Employee".')
    def click_create_employee(self):
        """Click create employee button"""
        self.click_on_element(selector=self.BUTTON_CREATE_EMPLOYEE)
