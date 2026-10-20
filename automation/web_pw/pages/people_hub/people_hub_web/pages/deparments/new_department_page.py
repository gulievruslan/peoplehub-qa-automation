"""Module contains page object for the PeopleHub new departments page."""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.departments.new_department_locators import (
    NewDepartmentsPageLocatorsPW,
)


class NewDepartmentPage(BasePeopleHubPage, NewDepartmentsPageLocatorsPW):
    """Page Object for the PeopleHub new department."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub new department.

        Args:
            page: Page Object for the PeopleHub departments
        """
        super().__init__(page=page, url="departments/new")

    @step('Check page content displaying')
    def check_new_department_content_displaying(self):
        """Check page content displaying"""
        self.soft_check_elements_visibility(
            locators=[
                self.TITLE_ADD_DEPARTMENT,
                self.TITLE_CREATE_NEW_DEPARTMENT,
                self.TITLE_DEPARTMENT_INFORMATION,
                self.BUTTON_CREATE_DEPARTMENT,
                self.BUTTON_CANCEL,
                self.INPUT_FIELD_DEPARTMENT
            ]
        )

    @step('Click on input field')
    def click_input_field(self):
        """Click on input field"""
        self.click_on_element(selector=self.INPUT_FIELD_DEPARTMENT)

    @step("Fill in new department: {new_department}")
    def fill_new_department(self, department_name: str):
        """Fill in new department

        Args:
            department_name: New department name
        """
        self.clear_and_type_like_user(value=department_name, locator=self.INPUT_FIELD_DEPARTMENT)

    @step('Click button "Create Department".')
    def click_button_add_department(self):
        """Click button "Create Department"."""
        self.click_on_element(selector=self.BUTTON_CREATE_DEPARTMENT)
