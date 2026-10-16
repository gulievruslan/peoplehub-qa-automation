"""Framework configuration."""

from pathlib import Path


class Config:
    """Configuration for test execution."""
    debug: bool = False
    log_level: str = "INFO"
    test_data_dir: Path = Path("test_data").absolute()
    temp_dir: Path = test_data_dir / "temp"
    csv_dir: Path = temp_dir / "csv"
    timeout: int = 30
