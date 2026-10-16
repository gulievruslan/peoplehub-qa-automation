"""Page Object for the PeopleHub dashboard."""

from playwright.sync_api import Page

from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage


class DashboardPage(BasePeopleHubPage):
    """Page Object for the PeopleHub dashboard."""

    def __init__(self, page: Page):
        """Initialize the Page Object for the PeopleHub dashboard.

        Args:
            page: Page Object for the PeopleHub dashboard
        """
        super().__init__(page=page, url="dashboard")

