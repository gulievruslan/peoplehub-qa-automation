"""Base class for all pages, providing common methods such as navigation and screenshot comparison."""

from pathlib import Path

import pytest
from allure import attach, attachment_type, step
from PIL import Image
from playwright.sync_api import Locator, Page


class BasePage:
    """Base page class providing common methods for navigation and visual comparison."""

    def __init__(self, page: Page, url: str | None = None):
        """Initialize the base page.

        Args:
            page: Playwright Page instance.
            url: Optional page URL.
        """
        self.page = page
        self.url = url

    @step("Open page URL")
    def get(self, url: str | None = None) -> "BasePage":
        """Open page URL.

        Args:
            url: Optional page URL.
        """
        target_url = url or self.url

        if target_url is None:
            raise ValueError("URL is not set. Provide a URL when creating the page.")

        self.page.goto(target_url)

        return self

    @staticmethod
    def _compare_images(
        baseline_path: str,
        current_path: str,
        diff_path: str,
        base_name: str,
        current_name: str,
        diff_name: str,
    ):
        """Compare images and attach the results to the Allure report.

        Args:
            baseline_path: Path to the baseline screenshot.
            current_path: Path to the current screenshot.
            diff_path: Path to the difference image.
            base_name: Baseline screenshot filename.
            current_name: Current screenshot filename.
            diff_name: Difference image filename.
        """
        baseline_img = Image.open(baseline_path).convert("RGB")
        current_img = Image.open(current_path).convert("RGB")

        diff_check = Image.new("RGB", current_img.size, (0, 0, 0))

        diff = current_img.copy()

        width, height = current_img.size
        has_diff = False

        if baseline_img.size != current_img.size:
            has_diff = True

            for i in range(width):
                for j in range(height):
                    diff_check.putpixel((i, j), (255, 0, 0))
                    diff.putpixel((i, j), (255, 0, 0))
        else:
            for i in range(width):
                for j in range(height):
                    baseline_pixel = baseline_img.getpixel((i, j))
                    current_pixel = current_img.getpixel((i, j))

                    if baseline_pixel != current_pixel:
                        diff_check.putpixel((i, j), (255, 0, 0))
                        diff.putpixel((i, j), (255, 0, 0))
                        has_diff = True

        if not has_diff:
            return

        diff.save(diff_path)

        with open(baseline_path, "rb") as f:
            attach(f.read(), name=base_name, attachment_type=attachment_type.PNG)

        with open(current_path, "rb") as f:
            attach(f.read(), name=current_name, attachment_type=attachment_type.PNG)

        with open(diff_path, "rb") as f:
            attach(f.read(), name=diff_name, attachment_type=attachment_type.PNG)

        pytest.fail(f"Visual differences detected! See {diff_path}")

    @step("Check screenshot for differences from the baseline image")
    def check_screenshot_diff(self, baseline_path: str, locator: Page | Locator):
        """Compare a screenshot with its baseline image.

        Args:
            baseline_path: Path to the baseline screenshot.
            locator: Playwright Page or Locator instance.
        """
        with step("Check whether the baseline screenshot exists"):
            baseline_path_obj = Path(baseline_path)

            if not baseline_path_obj.exists():
                with step("Save a new baseline screenshot"):
                    baseline_path_obj.parent.mkdir(parents=True, exist_ok=True)
                    locator.screenshot(path=baseline_path)
                    pytest.fail(f"Baseline screenshot was not found and has been created: {baseline_path}")

        with step("Capture the current screenshot"):
            screenshot_dir = Path("test_data/temp")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            base_name = Path(baseline_path).name
            current_name = base_name.rsplit(sep=".")[0] + "_current.png"
            current_path = screenshot_dir / current_name

            locator.screenshot(path=current_path)

        with step("Compare screenshots"):
            diff_name = base_name.rsplit(sep=".")[0] + "_diff.png"
            diff_path = screenshot_dir / diff_name
            self._compare_images(
                str(baseline_path),
                str(current_path),
                str(diff_path),
                base_name,
                current_name,
                diff_name,
            )
