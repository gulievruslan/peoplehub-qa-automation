from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_base_url: str = "http://127.0.0.1:8000"

    peoplehub_admin_email: str
    peoplehub_admin_password: SecretStr

    peoplehub_hr_email: str
    peoplehub_hr_password: SecretStr

    peoplehub_employee_email: str
    peoplehub_employee_password: SecretStr


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()