from dataclasses import dataclass
from pydantic import SecretStr

from automation.config.settings import get_settings


@dataclass(frozen=True)
class TestUser:
    email: str
    password: SecretStr


settings = get_settings()

ADMIN = TestUser(
    email=settings.peoplehub_admin_email,
    password=settings.peoplehub_admin_password,
)

HR = TestUser(
    email=settings.peoplehub_hr_email,
    password=settings.peoplehub_hr_password,
)

EMPLOYEE = TestUser(
    email=settings.peoplehub_employee_email,
    password=settings.peoplehub_employee_password,
)