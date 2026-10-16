"""Public interface for the custom Playwright utilities."""

from automation.web_playwright_custom.pages.base_pw.constants import (
    MILLISECONDS_MULTIPLIER,
    TIME_FAST,
    TIME_ULTRA_FAST,
    TIMEOUT_PW,
)
from automation.web_playwright_custom.pages.base_pw.locators import LocatorPW, PlaywrightLocator
from automation.web_playwright_custom.pages.base_pw.pages import BasePagePW
from automation.web_playwright_custom.pages.base_pw.utils import business_check_to_broken
from automation.web_playwright_custom.pages.base_pw.utils.get_description import get_description

__all__ = (
    "MILLISECONDS_MULTIPLIER",
    "TIME_FAST",
    "TIME_ULTRA_FAST",
    "TIMEOUT_PW",
    "LocatorPW",
    "PlaywrightLocator",
    "BasePagePW",
    "business_check_to_broken",
    "get_description",
)