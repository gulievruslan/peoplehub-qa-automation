"""Factory for configuring local Playwright browser launch options."""

import os
import tomllib
from pathlib import Path
from typing import Any

from automation.web_pw import PWConfig


class PWLocalOptionsFactory:
    """Factory for local Playwright browser launch and context options."""

    @staticmethod
    def _get_config() -> dict[str, Any]:
        """Load Playwright settings from pyproject.toml."""
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "pyproject.toml"

        with config_path.open("rb") as config_file:
            config = tomllib.load(config_file)

        return config.get("tool", {}).get("peoplehub", {}).get("playwright", {})

    @staticmethod
    def get_launch_args() -> dict[str, Any]:
        """Return arguments for launching the local browser."""
        config = PWLocalOptionsFactory._get_config()
        is_ci = os.getenv("CI", "").lower() == "true"

        args = PWConfig.DEFAULT_ARGS.copy()
        if not is_ci:
            args.append("--start-maximized")

        return {
            "args": args,
            "headless": True if is_ci else config.get("headless", False),
            "slow_mo": config.get("slow_mo", 0),
        }

    @staticmethod
    def get_context_args() -> dict[str, Any]:
        """Return arguments for creating a browser context."""
        return {"no_viewport": True, "accept_downloads": True}