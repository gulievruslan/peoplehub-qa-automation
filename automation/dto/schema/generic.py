"""Generic DTO classes for PeopleHub API automation."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class PeopleHubDTO(BaseModel):
    """Base DTO for PeopleHub API automation."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Convert DTO to a dictionary suitable for API requests.

        Unset and None values are excluded, and field aliases are used.
        """
        return super().model_dump(
            *args,
            exclude_unset=True,
            exclude_none=True,
            by_alias=True,
            **kwargs,
        )