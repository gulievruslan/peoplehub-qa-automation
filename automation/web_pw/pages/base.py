"""Базовый класс для всех страниц — предоставляет общие методы (переход, скриншоты и т.д.)."""

from pathlib import Path
from typing import TypeVar

import pytest
from allure import attach, attachment_type, step
from PIL import Image
from playwright.sync_api import Locator, Page

from automation.custom.config import Config

PagePW = TypeVar(name="PagePW", bound=Page)


class BasePage:
    """Базовый класс страницы с общими методами: открытие URL, проверка визуальных различий."""

    def __init__(self, page: PagePW, url: str | None = None) -> None:
        """Инициализация базовой страницы.

        Args:
            page: Экземпляр Playwright Page.
            url: Опциональный URL страницы.
        """
        self.page = page
        self.url = Config.web_url if url is None else url

    @step("Открыть URL страницы")
    def get(self) -> "BasePage":
        """Открыть URL."""
        if self.url is None:
            raise ValueError("URL не установлен. Укажите url при создании страницы.")
        self.page.goto(self.url)
        return self

    @staticmethod
    def _compare_images(
            baseline_path: str,
            current_path: str,
            diff_path: str,
            base_name: str,
            current_name: str,
            diff_name: str,
    ) -> None:
        """Сравнить изображения и прикрепить результаты к отчету.

        Args:
            baseline_path: Путь до базового скриншота.
            current_path: Путь до текущего скриншота.
            diff_path: Путь до скриншота различий.
            base_name: Имя базового файла.
            current_name: Имя текущего файла.
            diff_name: Имя файла различий.
        """
        baseline_img = Image.open(baseline_path).convert("RGB")
        current_img = Image.open(current_path).convert("RGB")

        baseline_pixels = baseline_img.load()
        current_pixels = current_img.load()

        diff_check = Image.new("RGB", current_img.size, (0, 0, 0))
        diff_check_pixels = diff_check.load()

        diff = current_img.copy()
        diff_pixels = diff.load()

        width, height = current_img.size
        has_diff = False

        if baseline_img.size != current_img.size:
            has_diff = True

            for i in range(width):
                for j in range(height):
                    diff_check_pixels[i, j] = (255, 0, 0)
                    diff_pixels[i, j] = (255, 0, 0)

        else:
            for i in range(width):
                for j in range(height):
                    br, bg, bb = baseline_pixels[i, j]
                    cr, cg, cb = current_pixels[i, j]

                    if br != cr or bg != cg or bb != cb:
                        diff_check_pixels[i, j] = (255, 0, 0)
                        diff_pixels[i, j] = (255, 0, 0)
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

        pytest.fail(f"Обнаружены визуальные различия! См. {diff_path}")

    @step("Проверить скриншот на наличие разницы с эталонным изображением.")
    def check_screenshot_diff(self, baseline_path: str, locator: Page | Locator) -> None:
        """Проверить скриншот на наличие разницы с эталонным изображением.

        Args:
            baseline_path: путь до эталона
            locator: объект Page or Locator
        """

        with step("Проверить наличие базового скриншота"):
            baseline_path_obj = Path(baseline_path)

            if not baseline_path_obj.exists():
                with step("Сохранить новый эталонный скриншот"):
                    baseline_path_obj.parent.mkdir(parents=True, exist_ok=True)
                    locator.screenshot(path=baseline_path)
                    pytest.fail(f"Эталонный скриншот не найден и был создан: {baseline_path}")

        with step("Сделать скриншот по переданному локатору"):
            screenshot_dir = Path("test_data/temp")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            base_name = Path(baseline_path).name
            current_name = base_name.rsplit(sep=".")[0] + "_current.png"
            current_path = screenshot_dir / current_name

            locator.screenshot(path=current_path)

        with step("Cравнить изображения"):
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
