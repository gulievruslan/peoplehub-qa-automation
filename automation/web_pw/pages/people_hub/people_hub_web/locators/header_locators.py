"""Locators for the PeopleHub header."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class HeaderLocatorsPW:
    """Locators for elements on the header."""

    BUTTON_LOGOUT = LocatorPW(name="Logout button", selector="//button[@class='logout-button']")
