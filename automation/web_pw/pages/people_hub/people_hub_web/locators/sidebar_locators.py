"""Locators for the PeopleHub sidebar."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class SidebarLocatorsPW:
    """Locators for elements on the sidebar."""

    LOGO = LocatorPW(name="Sidebar logo", selector='//*[@class="sidebar-logo"]')
