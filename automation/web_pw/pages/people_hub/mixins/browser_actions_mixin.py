"""Browser interaction helpers for tabs, JavaScript dialogs, storage, and URLs."""

import json
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Literal

from automation.custom.allure.custom_allure import step
from automation.custom.asserts.soft_assert import soft_assert
from automation.web_pw.pages.people_hub.constants import TIME_ACTION

StorageType = Literal["local", "session"]


if TYPE_CHECKING:
    from automation.web_playwright_custom.pages.base_pw import BasePagePW

    class _Base(BasePagePW):
        """Base class used for static type checking."""

else:

    class _Base:
        """Runtime base class for the mixin."""


class BrowserActionsMixin(_Base):
    """Reusable browser actions for PeopleHub Page Objects."""

    @step(title="Refresh the current page")
    def refresh(
        self,
        wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] | None = "domcontentloaded",
    ) -> None:
        """Reload the current page.

        Args:
            wait_until: Lifecycle state to wait for after reloading.
        """
        self.page.reload(wait_until=wait_until)

    @step(title='Switch to the tab whose URL contains "{url_part}"')
    def switch_to_tab_by_url(self, url_part: str) -> None:
        """Bring the first tab containing the specified URL fragment to the foreground.

        Args:
            url_part: URL fragment used to identify the tab.

        Raises:
            RuntimeError: If no matching tab is found.
        """
        if not url_part:
            raise ValueError("The URL fragment must not be empty.")

        for page in self.page.context.pages:
            if url_part in page.url:
                page.bring_to_front()
                return

        raise RuntimeError(f'No tab found with a URL containing "{url_part}".')

    @step(title="Switch to the tab at index {index}")
    def switch_to_tab_by_index(self, index: int) -> None:
        """Bring a tab at the specified zero-based index to the foreground.

        Args:
            index: Zero-based index of the tab.

        Raises:
            IndexError: If the index does not identify an open tab.
        """
        pages = self.page.context.pages

        if index < 0 or index >= len(pages):
            raise IndexError(f"Tab index {index} is out of range. Number of open tabs: {len(pages)}.")

        pages[index].bring_to_front()

    @step(title="Close the current tab")
    def close_current_tab(self) -> None:
        """Close the current tab and bring a neighboring tab to the foreground.

        Raises:
            RuntimeError: If the current tab is the only open tab.
        """
        context = self.page.context
        pages = context.pages

        if len(pages) <= 1:
            raise RuntimeError("Cannot close the only open tab.")

        current_index = pages.index(self.page)
        self.page.close()

        remaining_pages = context.pages
        if remaining_pages:
            next_index = min(current_index, len(remaining_pages) - 1)
            remaining_pages[next_index].bring_to_front()

    @step(title='Close the tab whose URL contains "{url_part}"')
    def close_tab_by_url(self, url_part: str) -> None:
        """Close the first tab containing the specified URL fragment.

        Args:
            url_part: URL fragment used to identify the tab.

        Raises:
            RuntimeError: If no matching tab is found.
        """
        if not url_part:
            raise ValueError("The URL fragment must not be empty.")

        context = self.page.context
        target_page = next((page for page in context.pages if url_part in page.url), None)

        if target_page is None:
            raise RuntimeError(f'No tab found with a URL containing "{url_part}".')

        was_current_page = target_page == self.page
        target_page.close()

        if was_current_page:
            remaining_pages = context.pages
            if remaining_pages:
                remaining_pages[0].bring_to_front()

    @staticmethod
    def _get_storage_name(storage_type: StorageType) -> str:
        """Return the browser storage object name for a supported storage type."""
        if storage_type == "local":
            return "localStorage"
        if storage_type == "session":
            return "sessionStorage"
        raise ValueError(f'Unsupported storage type "{storage_type}". Use "local" or "session".')

    @step(title="Get data from browser storage")
    def get_storage_data(self, storage_type: StorageType = "local") -> dict[str, str]:
        """Read all key-value pairs from localStorage or sessionStorage.

        Args:
            storage_type: Browser storage type.

        Returns:
            A dictionary containing the storage keys and string values.
        """
        storage_name = self._get_storage_name(storage_type)
        script = """
            storageName => {
                const storage = window[storageName];
                const result = {};

                for (let index = 0; index < storage.length; index++) {
                    const key = storage.key(index);
                    if (key !== null) {
                        result[key] = storage.getItem(key);
                    }
                }

                return result;
            }
        """
        return self.page.evaluate(expression=script, arg=storage_name)

    @step(title="Insert data into browser storage")
    def insert_storage_data(
        self,
        storage_type: StorageType = "local",
        data: dict[str, Any] | None = None,
    ) -> None:
        """Insert or update key-value pairs in browser storage.

        Strings are stored as-is; other values are serialized as JSON.

        Args:
            storage_type: Browser storage type.
            data: Key-value pairs to insert or update.
        """
        if not data:
            return

        storage_name = self._get_storage_name(storage_type)

        for key, value in data.items():
            serialized_value = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            self.page.evaluate(
                expression="([storageName, key, value]) => window[storageName].setItem(key, value)",
                arg=[storage_name, str(key), serialized_value],
            )

    @step(title="Clear selected keys from browser storage")
    def clear_storage_by_keys(
        self,
        storage_type: StorageType = "local",
        keys: str | Sequence[str] | None = None,
    ) -> None:
        """Remove selected keys from browser storage.

        Args:
            storage_type: Browser storage type.
            keys: A single key or a sequence of keys to remove.
        """
        if keys is None:
            return

        storage_name = self._get_storage_name(storage_type)
        keys_to_remove = (keys,) if isinstance(keys, str) else keys

        for key in keys_to_remove:
            self.page.evaluate(
                expression="([storageName, key]) => window[storageName].removeItem(key)",
                arg=[storage_name, key],
            )

    @step(title="Accept JavaScript dialog")
    def accept_alert(self, action: Callable[[], None], timeout: float = TIME_ACTION) -> None:
        """Accept a JavaScript dialog triggered by an action.

        Args:
            action: Callable that triggers the dialog.
            timeout: Maximum time to wait for the dialog, in milliseconds.
        """
        with self.page.expect_event("dialog", timeout=timeout) as dialog_info:
            action()

        dialog_info.value.accept()

    @step(title="Dismiss JavaScript dialog")
    def dismiss_alert(self, action: Callable[[], None], timeout: float = TIME_ACTION) -> None:
        """Dismiss a JavaScript dialog triggered by an action.

        Args:
            action: Callable that triggers the dialog.
            timeout: Maximum time to wait for the dialog, in milliseconds.
        """
        with self.page.expect_event("dialog", timeout=timeout) as dialog_info:
            action()

        dialog_info.value.dismiss()

    @step(title="Enter text into JavaScript prompt")
    def send_keys_to_alert(
        self,
        text: str,
        action: Callable[[], None],
        timeout: float = TIME_ACTION,
    ) -> None:
        """Submit text to a JavaScript prompt triggered by an action.

        Args:
            text: Text to submit to the prompt.
            action: Callable that triggers the prompt.
            timeout: Maximum time to wait for the dialog, in milliseconds.
        """
        with self.page.expect_event("dialog", timeout=timeout) as dialog_info:
            action()

        dialog_info.value.accept(prompt_text=text)

    @step(title="Check exact URL match")
    def check_current_url(self, expected_url: str) -> None:
        """Soft-check that the current URL exactly matches the expected URL."""
        actual_url = self.page.url
        soft_assert(
            condition=actual_url == expected_url,
            message=f'Current URL "{actual_url}" does not match expected URL "{expected_url}".',
        )

    @step(title="Check the number of open tabs")
    def check_tabs_count(self, expected_count: int) -> None:
        """Soft-check the number of open tabs."""
        if expected_count < 0:
            raise ValueError("Expected tab count must not be negative.")

        actual_count = len(self.page.context.pages)
        soft_assert(
            condition=actual_count == expected_count,
            message=f"Expected {expected_count} open tabs, but found {actual_count}.",
        )