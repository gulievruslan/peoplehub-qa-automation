"""Module contains page object for the PeopleHub "Employee Profile". page"""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.employees.employee_profile_locators import (
    EmployeeProfilePageLocatorsPW,
)


class EmployeeProfilePage(BasePeopleHubPage, EmployeeProfilePageLocatorsPW):
    """Page Object for the PeopleHub employee profile."""

    def __init__(self, page: Page, employee_id: int):
        """Initialize the Page Object for the PeopleHub employees.

        Args:
            page: Page Object for the PeopleHub employees
        """
        super().__init__(page=page, url=f"employees/{employee_id}")

    @step('Check employee profile')
    def check_employee_profile(
        self, first_name: str, last_name: str, email: str, position: str, department_name: str, phone: str | None = None
    ):
        """Check employee profile page."""
        self.soft_check_elements_visibility(
            locators=[
                self.TITLE_NAME_SURNAME.format(name_surname=f'{first_name} {last_name}'),
                self.TEXT_POSITION.format(position=position),
                self.TEXT_EMPLOYEE_CONTENT_DYNAMIC.format(field='First Name', field_value=first_name),
                self.TEXT_EMPLOYEE_CONTENT_DYNAMIC.format(field='Last Name', field_value=last_name),
                self.TEXT_EMPLOYEE_CONTENT_DYNAMIC.format(field='Email', field_value=email),
                self.TEXT_EMPLOYEE_CONTENT_DYNAMIC.format(field='Phone', field_value=phone),
                self.TEXT_EMPLOYEE_CONTENT_DYNAMIC.format(field='Position', field_value=position),
                self.TEXT_EMPLOYEE_DEPARTMENT.format(department_name=department_name),
            ]
        )