"""Module providing reusable checks for UI elements and structures."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from automation.custom.allure_custom.custom_allure import step
from automation.web_pw.pages.people_hub.constants import TIME_ACTION
from automation.web_pw.pages.people_hub.mixins import BaseChecksMixin

if TYPE_CHECKING:
    from automation.web_playwright_custom.pages.base_pw import BasePagePW

    class _Base(BaseChecksMixin, BasePagePW):
        """Base class used for static type checking."""

else:

    class _Base:
        """Runtime base class for the mixin."""


class ChecksMixin(_Base):
    """Reusable checks for UI elements and structures."""

    @step(title="Check buttons")
    def soft_check_buttons(
        self,
        buttons: Iterable[tuple[str, str | None, bool]],
        timeout: float = TIME_ACTION,
    ):
        """Soft-check button visibility and enabled state.

        Each tuple contains the button name, an optional test ID, and the expected enabled state.
        Buttons with an empty name are skipped.

        Args:
            buttons: Iterable of (name, data_testid, is_enabled) tuples.
            timeout: Maximum time to wait for each check, in milliseconds.
        """
        for name, data_testid, is_enabled in buttons:
            if not name:
                continue

            with step(title=f'Check button "{name}"'):
                description = f'Button "{name}"'

                if data_testid:
                    locator_button = self.page.get_by_test_id(test_id=data_testid)
                else:
                    locator_button = self.page.get_by_role(role="button", name=name)

                locator_button = locator_button.describe(description=description)

                self.soft_check_visibility(
                    locator=locator_button,
                    timeout=timeout,
                )
                self.soft_check_element_enabled(
                    locator=locator_button,
                    is_enabled=is_enabled,
                    timeout=timeout,
                )