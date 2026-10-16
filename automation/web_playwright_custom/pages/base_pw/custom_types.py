"""Data types.

Notes:
    LoggedObjects: Types of objects that support logging.
"""

from playwright.sync_api import APIResponse, Locator, Page

from automation.web_playwright_custom.pages.base_pw.locators.locators import LocatorPW

type LoggedObjects = LocatorPW | Locator | Page | APIResponse