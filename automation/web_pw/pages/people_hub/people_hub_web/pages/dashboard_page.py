"""Module contains page object for the PeopleHub "Dashboard". page"""
from playwright.sync_api import Page

from automation.custom.allure_custom.custom_allure import step
from automation.dto.schema.payroll_models import PayrollItemInfo
from automation.tests.web.enums import DashboardPageCards, DashboardPageTitles
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.people_hub_web.locators.dashboard_locators import DashboardPageLocatorsPW


class DashboardPage(BasePeopleHubPage, DashboardPageLocatorsPW):
    """Page Object for the PeopleHub dashboard."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub dashboard.

        Args:
            page: Page Object for the PeopleHub dashboard
        """
        super().__init__(page=page, url="dashboard")


    @step('Check titles displaying')
    def check_titles_displaying(self):
        """Check titles displaying."""
        for title in DashboardPageTitles:
            self.soft_check_visibility(locator=self.TITLE_DASHBOARD_DYNAMIC.format(title=title), is_need_scroll=True)

    @step('Check cards displaying')
    def check_cards_displaying(self):
        """Check cards displaying."""
        for card in DashboardPageCards:
            self.soft_check_visibility(locator=self.ELEMENT_CARD_DYNAMIC.format(card=card), is_need_scroll=True)

    @step('Check payroll completion progress bar displaying')
    def check_payroll_completion_progress_bar_displaying(self):
        """Check payroll completion progress bar displaying."""
        self.check_visibility(locator=self.PROGRESS_BAR_PAYROLL)

    @step('Employee "{name_surname}" salary displaying')
    def check_employee_salary_displaying(self, employee_data: dict[str, int | float]):
        """Check employee salary displaying.

        Args:
            employee_data: Employee name and salary data
        """
        for name_surname, salary in employee_data.items():
            self.soft_check_visibility(
                locator=self.TEXT_EMPLOYEE_SALARY.format(name_surname=name_surname, salary=f"{salary:,.0f}"),
                is_need_scroll=True
            )

    @step('Check employees payment data displaying')
    def check_employee_payment_displaying(self, employment_data: dict[str, int | float]):
        """Check employees payment data displaying.

        Args:
            employment_data: Employee name and payment data
        """
        self.soft_check_elements_visibility(
            locators=[
                self.TEXT_COUNT_TOTAL_PAYROLL.format(value=f"{employment_data['total_payroll']:,.0f}"),
                self.TEXT_EMPLOYEES_PAID_COUNT.format(count=employment_data['employees_paid']),
                self.TEXT_EMPLOYEES_AVERAGE_SALARY.format(salary=f"{employment_data['average_salary']:,.0f}")
            ]
        )

    @step('Check employee salary statistics displaying')
    def check_employee_salary_statistics_displaying(
        self, latest_salary: float, paid_amount: float, records_count: int
    ):
        """Check employee salary statistics displaying.

        Args:
            latest_salary: Latest salary data
            paid_amount: Paid amount data
            records_count: Record count data
        """
        self.soft_check_elements_visibility(
            locators=[
                self.TEXT_LATEST_SALARY_AMOUNT.format(latest_salary=f"{latest_salary:,.0f}"),
                self.TEXT_TOTAL_PAID_AMOUNT.format(paid_amount=f"{paid_amount:,.0f}"),
                self.TEXT_PAYROLL_RECORDS_COUNT.format(records_count=records_count)
            ]
        )

    @step("Check payroll items displaying")
    def check_payroll_items_displaying(self, payroll: list[PayrollItemInfo]):
        """Check that month, salary, and status are displayed for every payroll item.

        Args:
            payroll: Payroll items to check.
        """
        locators = [
            locator for item in payroll for locator in (
                self.TEXT_PAYROLL_MONTH.format(
                    month=item.month,
                    year=item.year,
                ),
                self.TEXT_PAYROLL_SALARY.format(
                    month=item.month,
                    year=item.year,
                    salary=f"{item.salary:,.0f}",
                ),
                self.TEXT_PAYROLL_STATUS.format(
                    month=item.month,
                    year=item.year,
                    status=item.status.capitalize(),
                ),
            )
        ]

        self.soft_check_elements_visibility(locators=locators)