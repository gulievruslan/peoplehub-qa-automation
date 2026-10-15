import os
from datetime import UTC, datetime, timedelta
from typing import Any, cast

import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not configured"
    )

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=30),
) -> str:
    payload = data.copy()

    expire = datetime.now(UTC) + expires_delta
    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    return cast(dict[str, Any], payload)