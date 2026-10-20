"""Module contains page object for the PeopleHub "Employees". page"""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.employees.employee_locators import (
    EmployeesPageLocatorsPW,
)


class EmployeesPage(BasePeopleHubPage, EmployeesPageLocatorsPW):
    """Page Object for the PeopleHub employees."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub employees.

        Args:
            page: Page Object for the PeopleHub employees
        """
        super().__init__(page=page, url="employees")

    @step('Check employee content displaying')
    def check_employee_content_displaying(
        self, name_surname: str, email: str, position: str, status: str, department: str
    ):
        """Check the employee content displaying"""
        self.soft_check_elements_visibility(
            locators=[
                self.TITLE_EMPLOYEES,
                self.TITLE_MANAGE_EMPLOYEES,
                self.BUTTON_ADD_EMPLOYEE,
                self.TABLE_EMPLOYEES,
                self.FIELD_INPUT_SEARCH_EMPLOYEES,
                self.DROPDOWN_ALL_STATUSES,
                self.TEXT_NAME_SURNAME.format(name_surname=name_surname),
                self.TEXT_EMAIL.format(email=email),
                self.TEXT_POSITION.format(position=position),
                self.TEXT_STATUS.format(status=status, name_surname=name_surname),
                self.TEXT_DEPARTMENT.format(department=department),
            ]
        )

    @step('Click button "+ Add Employee".')
    def click_add_employee(self):
        """Click add employee button"""
        self.click_on_element(selector=self.BUTTON_ADD_EMPLOYEE)

    @step('Click on "Search Employees..." field.')
    def click_field_search_employees(self):
        """Click on search employees field"""
        self.click_on_element(selector=self.FIELD_INPUT_SEARCH_EMPLOYEES)

    @step('Fill in employee name and surname')
    def fill_employee_and_surname(self, name_surname: str):
        """Fill employee name and surname

        Args:
            name_surname: Name and surname of employee
        """
        self.clear_and_type_like_user(locator=self.FIELD_INPUT_SEARCH_EMPLOYEES, value=name_surname)

    @step('Check employee data displaying after searching')
    def check_employee_data_displaying_after_searching(
        self, name_surname: str, email: str, position: str, status: str, department: str
    ):
        """Fill employee name and surname

        Args:
            name_surname: Name and surname of employee
            email: Employee email
            position: Employee position
            status: Employee status
            department: Employee department
        """
        self.soft_check_elements_visibility(
            locators=[
                self.TEXT_NAME_SURNAME.format(name_surname=name_surname),
                self.TEXT_EMAIL.format(email=email),
                self.TEXT_POSITION.format(position=position),
                self.TEXT_STATUS.format(status=status, name_surname=name_surname),
                self.TEXT_DEPARTMENT.format(department=department),
                self.TEXT_EMPLOYEE_COUNT.format(count=1),
            ]
        )
