"""Fixtures for configuring and running PeopleHub Playwright tests."""

from collections.abc import Generator
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from _pytest.reports import TestReport
from allure import attach, attachment_type
from playwright.sync_api import Browser, Page, Playwright, expect, sync_playwright

from automation.config.users import TestUser
from automation.custom.allure_custom.custom_allure import step
from automation.custom.logger.project_logger import logger
from automation.web_pw import PWLocalOptionsFactory
from automation.web_pw.pages.people_hub.pages.base_page import BasePeopleHubPage
from automation.web_pw.pages.people_hub.utils.auth import get_access_token

DEFAULT_TIMEOUT = 15_000
DEFAULT_FRONTEND_URL = "http://localhost:5173"
DEFAULT_DASHBOARD_URL = f"{DEFAULT_FRONTEND_URL}/dashboard"
DEFAULT_LOGIN_URL = f"{DEFAULT_FRONTEND_URL}/login"

_SCREENSHOT_MARKER = "_peoplehub_failure_screenshot_attached"
_PAGE_KEY = "_peoplehub_playwright_page"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    """Attach a screenshot to Allure when a Web test fails during execution."""
    outcome = yield
    report: TestReport = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page: Page | None = getattr(item, _PAGE_KEY, None)

    if page is None or page.is_closed():
        logger.warning("Cannot capture failure screenshot: Playwright page is unavailable.")
        return

    if getattr(item, _SCREENSHOT_MARKER, False):
        return

    try:
        attach(
            page.screenshot(full_page=True),
            name="Screenshot: test failure",
            attachment_type=attachment_type.PNG,
        )
        setattr(item, _SCREENSHOT_MARKER, True)
        logger.info("Attached failure screenshot for test: %s", item.nodeid)
    except Exception:
        logger.exception("Failed to attach failure screenshot for test: %s", item.nodeid)


@pytest.fixture(scope="session")
def browser_type_launch_args() -> dict[str, Any]:
    """Return arguments used to launch the local browser."""
    return PWLocalOptionsFactory.get_launch_args()


@pytest.fixture(scope="session")
def browser_context_args() -> dict[str, Any]:
    """Return default browser context arguments."""
    return PWLocalOptionsFactory.get_context_args()


@pytest.fixture(scope="class")
def pw_playwright() -> Generator[Playwright, None, None]:
    """Start Playwright for a test class."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="class")
def pw_browser(
    pw_playwright: Playwright,
    browser_type_launch_args: dict[str, Any],
) -> Generator[Browser, None, None]:
    """Launch a local Chromium browser for a test class."""
    browser = pw_playwright.chromium.launch(**browser_type_launch_args)

    try:
        yield browser
    finally:
        browser.close()


@pytest.fixture
def pw_open_page(
    request: SubRequest,
    pw_browser: Browser,
    browser_context_args: dict[str, Any],
) -> Generator[BasePeopleHubPage, None, None]:
    """Create an isolated browser context and open the requested Page Object.

    Expected indirect parameters:
        (user, page_class)
        (user, page_class, {"authenticated": True, "url": "..."})
        (None, page_class, {"authenticated": False})

    Authentication is enabled by default. The access token is obtained through
    the PeopleHub API and installed in localStorage before the frontend loads.
    """
    param = getattr(request, "param", None)
    if not isinstance(param, (list, tuple)) or len(param) < 2:
        raise RuntimeError("Expected indirect parameters: (user, page_class, {kwargs})")

    user, page_class, *rest = param
    kwargs = dict(rest[0]) if rest else {}
    authenticated = kwargs.pop("authenticated", True)
    target_url = kwargs.pop("url", None)

    if authenticated and not isinstance(user, TestUser):
        raise TypeError("An authenticated test requires a TestUser instance.")

    page_url = target_url or (DEFAULT_DASHBOARD_URL if authenticated else DEFAULT_LOGIN_URL)

    context = pw_browser.new_context(**browser_context_args)
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(DEFAULT_TIMEOUT)
    expect.set_options(timeout=DEFAULT_TIMEOUT)

    page = None

    try:
        if authenticated:
            token = get_access_token(user=user)
            context.add_init_script(script=f'window.localStorage.setItem("access_token", {token!r});')

        page = context.new_page()
        setattr(request.node, _PAGE_KEY, page)

        target_page = page_class(page=page, **kwargs)

        with step(title=f"Open page: {page_class.__name__}"):
            page.goto(page_url)
            page.wait_for_load_state("domcontentloaded")

        yield target_page
    except Exception:
        if page is not None and not page.is_closed():
            try:
                attach(
                    page.screenshot(full_page=True),
                    name=f"Page setup failed: {page_class.__name__}",
                    attachment_type=attachment_type.PNG,
                )
            except Exception:
                logger.exception("Failed to capture setup screenshot")

        logger.exception("Failed to open page object: %s", page_class.__name__)
        raise
    finally:
        setattr(request.node, _PAGE_KEY, None)
        context.close()