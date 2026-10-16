"""Data types.

Notes:
    LoggedObjects: Types of objects that support logging.
"""

from typing import TypeAlias

from playwright.sync_api import APIResponse, Locator, Page

from automation.web_playwright_custom.pages.base_pw.locators.locators import LocatorPW

LoggedObjects: TypeAlias = LocatorPW | Locator | Page | APIResponse