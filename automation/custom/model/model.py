"""Helpers for converting Pydantic models into request payloads."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

JsonBody = Mapping[str, Any] | BaseModel | list[Any]
FormBody = Mapping[str, Any] | list[Any] | str | bytes | BaseModel
QueryParams = Mapping[str, Any] | BaseModel


def _dump(value: Any, dump_kwargs: dict[str, Any]) -> Any:
    """Recursively convert models inside a payload to plain Python data.

    Args:
        value: A model, a mapping, a list/tuple or any other value.
        dump_kwargs: Arguments passed to BaseModel.model_dump.

    Returns:
        The payload without BaseModel instances. Strings, bytes and other
        values are returned unchanged; tuples stay tuples (form pairs).
    """
    if isinstance(value, BaseModel):
        return value.model_dump(**dump_kwargs)
    if isinstance(value, Mapping):
        return {key: _dump(item, dump_kwargs) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        converted: list[Any] = [_dump(item, dump_kwargs) for item in value]
        return tuple(converted) if isinstance(value, tuple) else converted
    return value


def _query_value(value: Any) -> Any:
    """Convert a query parameter value to the form APIs usually expect.

    Args:
        value: A single query parameter value.

    Returns:
        "true"/"false" for booleans (requests would send "True"/"False"),
        the same conversion for list items, other values unchanged.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return [_query_value(item) for item in value]
    return value


def convert_models_to_request(
    json: JsonBody | None = None,
    data: FormBody | None = None,
    params: QueryParams | None = None,
    **kwargs: Any,
) -> tuple[Any, Any, Any]:
    """Convert Pydantic models in a request to JSON-compatible data.

    Models are dumped with mode="json" (datetime, UUID and Enum become strings)
    and by_alias=True. Both defaults can be overridden through kwargs.
    Models nested in dicts and lists are converted too. None stays None,
    and empty dicts/lists are passed through unchanged.

    Args:
        json: JSON body: a model, a dict or a list of them.
        data: Form body, string or bytes. Models and dicts are converted.
        params: Query parameters: a model or a dict. Booleans become "true"/"false".
        **kwargs: Arguments for BaseModel.model_dump,
            e.g. exclude_none=True, exclude_unset=True, by_alias=False.

    Returns:
        A tuple (json, data, params) ready to pass to requests.
    """
    dump_kwargs: dict[str, Any] = {"mode": "json", "by_alias": True, **kwargs}

    json_body: Any = _dump(json, dump_kwargs)
    form_body: Any = _dump(data, dump_kwargs)

    query: Any = _dump(params, dump_kwargs)
    if isinstance(query, Mapping):
        query = {key: _query_value(item) for key, item in query.items()}

    return json_body, form_body, query