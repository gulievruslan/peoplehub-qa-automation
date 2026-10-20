"""Locators for the PeopleHub "Dashboard" page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class DashboardPageLocatorsPW:
    """Locators for elements on "Dashboard" page."""
    PAGE_DASHBOARD = LocatorPW(name="Dashboard page", selector="//*[@class='dashboard-page']")
    TITLE_DASHBOARD_DYNAMIC = PAGE_DASHBOARD.child(name="Title: {title}", selector="//h2[text()='{title}']")
    ELEMENT_CARD_DYNAMIC = PAGE_DASHBOARD.child(name="Card element: {card}", selector="//*[text()='{card}']")
    PROGRESS_BAR_PAYROLL = LocatorPW(name="Dashboard progress value", selector=".dashboard-progress-value")
    TEXT_EMPLOYEE_SALARY = LocatorPW(
        name="Employee {name_surname} salary {salary}",
        selector="//*[@class='salary-employee-info']//*[text()='{name_surname}']/following::*[contains(., '{salary}')]"
    )
    TEXT_COUNT_TOTAL_PAYROLL = LocatorPW(
        name='Total payroll value {value}', selector="text=Total payroll >> .. >> text={value}"
    )
    TEXT_EMPLOYEES_PAID_COUNT = LocatorPW(
        name="Employees paid count {count}", selector="text=Employees paid >> .. >> text={count}"
    )
    TEXT_EMPLOYEES_AVERAGE_SALARY = LocatorPW(
        name='Employees average salary {salary}', selector="text=Average salary >> .. >> text={salary}"
    )
    TEXT_LATEST_SALARY_AMOUNT = LocatorPW(
        name='Latest salary amount: {latest_salary}',
        selector=".dashboard-card:has-text('Latest salary') >> strong:has-text('{latest_salary}')"
    )
    TEXT_TOTAL_PAID_AMOUNT = LocatorPW(
        name='Total paid amount: {paid_amount}',
        selector=".dashboard-card:has-text('Total paid') >> strong:has-text('{paid_amount}')"
    )
    TEXT_PAYROLL_RECORDS_COUNT = LocatorPW(
        name="Payroll record count: {records_count}",
        selector=".dashboard-card:has-text('Payroll Records') >> strong:has-text('{records_count}')"
    )
    TEXT_PAYROLL_MONTH = LocatorPW(
        name="Payroll month: {month} {year}",
        locator_fn=lambda page, month, year: (
            page.locator(".salary-by-employee-row")
            .filter(has=page.get_by_text(f"{month} {year}", exact=True))
            .locator(".salary-employee-info strong")
        ),
    )

    TEXT_PAYROLL_SALARY = LocatorPW(
        name="Payroll salary: {salary} for {month} {year}",
        locator_fn=lambda page, month, year, salary: (
            page.locator(".salary-by-employee-row")
            .filter(has=page.get_by_text(f"{month} {year}", exact=True))
            .locator(".salary-value")
            .filter(has_text=salary)
        ),
    )

    TEXT_PAYROLL_STATUS = LocatorPW(
        name="Payroll status: {status} for {month} {year}",
        locator_fn=lambda page, month, year, status: (
            page.locator(".salary-by-employee-row")
            .filter(has=page.get_by_text(f"{month} {year}", exact=True))
            .locator(".dashboard-approved")
            .get_by_text(status, exact=True)
        ),
    )
