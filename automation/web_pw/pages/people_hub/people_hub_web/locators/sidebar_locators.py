"""Locators for the PeopleHub sidebar."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class SidebarLocatorsPW:
    """Locators for elements on the sidebar."""

    LOGO = LocatorPW(name="Sidebar logo", selector=".sidebar-logo")
    ELEMENT_SIDEBAR_DYNAMIC = LocatorPW(
        name="Sidebar element {text}",
        locator_fn=lambda page, text: (page.locator(".sidebar-link").get_by_text(text, exact=True)),
    )
    ELEMENT_SIDEBAR_ACTIVE_DYNAMIC = LocatorPW(
        name="Active sidebar element {text}",
        locator_fn=lambda page, href_element, text: (
            page.locator(f".sidebar-link.active[href='/{href_element}']").get_by_text(text, exact=True)
        ),
    )
