"""Locators for the PeopleHub sign-in page."""

from automation.web_playwright_custom.pages.base_pw import LocatorPW


class AuthPageLocatorsPW:
    """Locators for elements on the sign-in page."""

    FIELD_ENTER_DYNAMIC = LocatorPW(name="{field_name} field", selector="#{field_name}")
    BUTTON_SIGN_IN = LocatorPW(name="Sign in button", selector='button[type="submit"]')
    TEXT_INVALID_CREDENTIALS = LocatorPW(
        name="Invalid credentials",
        selector="//*[@class='login-error' and @role='alert' and text()='Invalid email or password']"
    )
    TEXT_MANDATORY_FIELDS_REQUIRED = LocatorPW(
        name="Email and password are required.",
        selector="//*[@class='login-error' and @role='alert' and text()='Email and password are required.']"
    )
