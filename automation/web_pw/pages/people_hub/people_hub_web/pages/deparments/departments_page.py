"""Module contains page object for the PeopleHub "Departments" page."""

from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.tests.web.enums import DepartmentsButtonNames
from automation.web_pw.pages.people_hub.constants import TIME_WAIT
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.departments.deparments_locators import (
    DepartmentsPageLocatorsPW,
)


class DepartmentsPage(BasePeopleHubPage, DepartmentsPageLocatorsPW):
    """Page Object for the PeopleHub departments."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub departments.

        Args:
            page: Page Object for the PeopleHub departments
        """
        super().__init__(page=page, url="departments")

    @step('Check page content displaying')
    def check_page_content_displaying(self):
        """Check page content displaying"""
        self.soft_check_elements_visibility(
            locators=[
                self.TITLE_DEPARTMENTS_DYNAMIC,
                self.TEXT_TOOLTIP,
                self.BUTTON_PRIMARY_DEPARTMENT_DYNAMIC.format(button="+ Add Department"),
                self.TOOLBAR_DEPARTMENTS,
                self.TABLE_DEPARTMENTS
            ]
        )

    @step('Click button "{button}')
    def click_button_dynamic(self, button: DepartmentsButtonNames):
        """Click button

        Args:
            button: Button name
        """
        self.click_on_element(selector=self.BUTTON_PRIMARY_DEPARTMENT_DYNAMIC.format(button=button))

    @step('Click {department_name} "edit" button')
    def click_button_edit_department(self, department_name: str):
        """Click department "edit" button

        Args:
            department_name: Department name
        """
        self.click_on_element(selector=self.BUTTON_EDIT_DEPARTMENT.format(department_name=department_name))

    @step('Check department {department_name} displaying')
    def check_department_displaying(self, department_name: str):
        """Check department displaying

        Args:
            department_name: Department name
        """
        self.check_visibility(locator=self.TEXT_DEPARTMENT_NAME.format(department_name=department_name))

    @step('Check department {department_name} absence')
    def check_department_absence(self, department_name: str):
        """Check department absence

        Args:
            department_name: Department name
        """
        self.expect(
            target=self.TEXT_DEPARTMENT_NAME.format(department_name=department_name)
        ).to_be_hidden(timeout=TIME_WAIT)

    @step('Check department can not be empty warning')
    def check_department_can_not_be_empty(self):
        """Check department can not be empty warning"""
        self.check_visibility(locator=self.TEXT_DEPARTMENT_WARNING_EMPTY)

    @step('Edit department "{department_name}" to {new_department_name}')
    def edit_department(self, department_name: str, new_department_name: str):
        """Edit department.

        Args:
            department_name: Department name
            new_department_name: New department name
        """
        self.clear_and_type_like_user(
            locator=self.INPUT_FIELD_EDIT_DEPARTMENT.format(department_name=department_name),
            value=new_department_name,
        )

    @step('Delete department "{department_name}"')
    def delete_department(self, department_name: str, accept: bool = True):
        """Delete a department and handle the confirmation dialog.

        Args:
            department_name: Department name
            accept: Accept the confirmation dialog
        """
        self.handle_alert(
            action=lambda: self.click_on_element(
                selector=self.BUTTON_DELETE_DEPARTMENT.format(department_name=department_name)
            ),
            accept=accept,
        )

    @step('Click input field department')
    def click_input_field_department(self):
        """Click input field department"""
        self.click_on_element(selector=self.FIELD_INPUT_SEARCH_DEPARTMENTS)

    @step("Search department {department_name}")
    def search_for_department(self, department_name: str):
        """Search department

        Args:
            department_name: Department name
        """
        self.clear_and_type_like_user(locator=self.FIELD_INPUT_SEARCH_DEPARTMENTS, value=department_name)