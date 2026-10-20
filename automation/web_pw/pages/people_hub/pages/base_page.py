"""Composite base page class for PeopleHub UI Page Objects."""
from playwright.sync_api import Page

from automation.custom.config import Config
from automation.web_playwright_custom.pages.base_pw import BasePagePW
from automation.web_pw.pages.people_hub.mixins import (
    BaseActionsMixin,
    BaseChecksMixin,
    BrowserActionsMixin,
    WaiterActionsMixin,
)


class BasePeopleHubPage(BaseActionsMixin, BaseChecksMixin, BrowserActionsMixin, WaiterActionsMixin, BasePagePW):
    """Base class for PeopleHub Page Objects."""

    def __init__(self, page: Page, url: str):
        """Initialize the base page.

        Args:
            page: Playwright page object.
            url: Relative page URL.
        """
        super().__init__(page=page, url=f"{Config.base_url}/{url}")

