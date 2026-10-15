"""JSON validation helpers."""

from json import JSONDecodeError, loads
from typing import Any


def is_value_json(value: str | bytes | bytearray, **kwargs: Any) -> bool:
    """Check whether a value contains valid JSON."""
    try:
        loads(value, **kwargs)

        return True

    except (JSONDecodeError, TypeError, UnicodeDecodeError):
        return False