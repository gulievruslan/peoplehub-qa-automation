
"""Logging and Allure helpers for HTTP requests and responses."""

import json
import shlex
import textwrap
from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import allure
import requests

from automation.custom.logger.project_logger import logger


__all__ = ["log_request", "log_response"]

MASK: str = "***"
MAX_LOG_BODY_LENGTH: int = 5000

SENSITIVE_KEY_MARKERS: tuple[str, ...] = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "api-key",
    "apikey",
    "authorization",
    "cookie",
)

_TEXT_CONTENT_MARKERS: tuple[str, ...] = (
    "text/",
    "json",
    "xml",
    "x-www-form-urlencoded",
    "javascript",
    "yaml",
    "csv",
)


def _to_text(value: str | bytes) -> str:
    """Decode a header value to text."""
    return value.decode("latin-1") if isinstance(value, bytes) else value


def _header(headers: Mapping[str, str | bytes], name: str) -> str:
    """Get a header value as text."""
    value = next(
        (value for key, value in headers.items() if key.lower() == name.lower()),
        "",
    )
    return _to_text(value)


def _is_sensitive_key(key: str) -> bool:
    """Check whether a key name looks like it holds a secret."""
    lowered = key.lower()
    return any(marker in lowered for marker in SENSITIVE_KEY_MARKERS)


def _mask_data(value: Any) -> Any:
    """Recursively mask values of sensitive keys in parsed JSON."""
    if isinstance(value, Mapping):
        return {
            key: MASK if _is_sensitive_key(str(key)) else _mask_data(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_mask_data(item) for item in value]
    return value


def _mask_headers(headers: Mapping[str, str | bytes]) -> dict[str, str]:
    """Mask values of sensitive headers."""
    masked: dict[str, str] = {}

    for name, raw_value in headers.items():
        value = _to_text(raw_value)

        if not _is_sensitive_key(name):
            masked[name] = value
            continue

        scheme, _, rest = value.partition(" ")
        if name.lower() == "authorization" and rest:
            masked[name] = f"{scheme} {MASK}"
        else:
            masked[name] = MASK

    return masked


def _mask_pairs(query: str) -> list[tuple[str, str]]:
    """Parse a query string or form body and mask sensitive values."""
    return [
        (key, MASK if _is_sensitive_key(key) else value)
        for key, value in parse_qsl(query, keep_blank_values=True)
    ]


def _mask_url(url: str) -> str:
    """Mask credentials and sensitive query parameters in a URL."""
    parts = urlsplit(url)
    host = parts.netloc.rpartition("@")[2]
    netloc = f"{MASK}@{host}" if "@" in parts.netloc else parts.netloc
    query = urlencode(_mask_pairs(parts.query), safe="*") if parts.query else ""

    return urlunsplit((parts.scheme, netloc, parts.path, query, parts.fragment))


def _is_text_content(content_type: str) -> bool:
    """Check whether a content type is human-readable text."""
    return any(marker in content_type for marker in _TEXT_CONTENT_MARKERS)


def _render_text(text: str, content_type: str) -> str:
    """Pretty-print and mask a text body."""
    if "json" in content_type or text.lstrip().startswith(("{", "[")):
        try:
            return json.dumps(
                _mask_data(json.loads(text)),
                ensure_ascii=False,
                indent=2,
            )
        except ValueError:
            pass

    if "x-www-form-urlencoded" in content_type:
        return urlencode(_mask_pairs(text), safe="*")

    return text


def _render_body(
    body: bytes | str | None,
    content_type: str,
) -> tuple[str | None, bool]:
    """Convert a request or response body to loggable text."""
    if not body:
        return None, False

    lowered = content_type.lower()

    if lowered.startswith("multipart/"):
        return f"<multipart body, {len(body)} bytes>", False

    if isinstance(body, bytes):
        if lowered and not _is_text_content(lowered):
            return f"<binary body, {len(body)} bytes, {content_type}>", False

        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            return f"<binary body, {len(body)} bytes>", False
    else:
        text = body

    return _render_text(text=text, content_type=lowered), True


def _truncate(text: str, limit: int = MAX_LOG_BODY_LENGTH) -> str:
    """Shorten long text for the log; Allure attachments stay full."""
    if len(text) <= limit:
        return text

    return f"{text[:limit]}\n... <truncated, {len(text) - limit} more characters>"


def _format_headers(headers: Mapping[str, str]) -> str:
    """Render headers as 'Name: value' lines."""
    return "\n".join(f"{name}: {value}" for name, value in headers.items())


def _compose(
    title: str,
    headers: Mapping[str, str],
    body_text: str | None,
) -> str:
    """Build a readable, structured HTTP log message."""
    separator = "=" * 88
    section_separator = "-" * 88

    lines: list[str] = [
        "",
        separator,
        f"  {title}",
        separator,
    ]

    if headers:
        lines.extend(["", "  HEADERS", section_separator])
        lines.extend(textwrap.indent(_format_headers(headers), "    ").splitlines())

    if body_text:
        lines.extend(["", "  BODY", section_separator])
        lines.extend(
            textwrap.indent(_truncate(body_text), "    ").splitlines()
        )

    lines.extend(["", separator])
    return "\n".join(lines)


def _attach(text: str, name: str) -> None:
    """Attach text to the current Allure step as JSON when possible."""
    try:
        json.loads(text)
        attachment_type = allure.attachment_type.JSON
    except ValueError:
        attachment_type = allure.attachment_type.TEXT

    allure.attach(text, name=name, attachment_type=attachment_type)


def _to_curl(
    method: str,
    url: str,
    headers: Mapping[str, str],
    body_text: str | None,
    is_insecure: bool,
) -> str:
    """Build a cURL command for reproducing a request with secrets masked."""
    parts: list[str] = ["curl", "-X", method, shlex.quote(url)]

    if is_insecure:
        parts.append("--insecure")

    for name, value in headers.items():
        if name.lower() != "content-length":
            parts += ["-H", shlex.quote(f"{name}: {value}")]

    if body_text:
        parts += ["--data-raw", shlex.quote(body_text)]

    return " \\\n  ".join(parts)

def log_request(
    request: requests.PreparedRequest,
    needs_allure: bool = True,
    is_insecure: bool = False,
) -> None:
    """Log a prepared request and optionally attach it to Allure."""
    method: str = request.method or "GET"
    url: str = _mask_url(request.url or "")
    headers: dict[str, str] = _mask_headers(request.headers)
    content_type: str = _header(request.headers, "Content-Type")

    raw_body: Any = request.body
    if raw_body is None or isinstance(raw_body, (bytes, str)):
        body_text, is_real_body = _render_body(
            body=raw_body,
            content_type=content_type,
        )
    else:
        body_text, is_real_body = "<streamed body>", False

    title: str = f"Request: {method} {url}"

    message = (
        f"\n<bold><cyan>HTTP REQUEST</cyan></bold> | "
        f"<blue><bold>{method}</bold></blue> {url}\n"
        f"<dim>Headers:</dim>"
    )

    for key, value in headers.items():
        message += f"\n  <cyan>{key}</cyan>: {value}"

    if body_text:
        message += f"\n<dim>Body:</dim>\n{body_text}"

    logger.opt(colors=True).info(message)

    if not needs_allure:
        return

    with allure.step(title):
        _attach(text=_format_headers(headers), name="Request headers")

        if body_text:
            _attach(text=body_text, name="Request body")

        _attach(
            text=_to_curl(
                method=method,
                url=url,
                headers=headers,
                body_text=body_text if is_real_body else None,
                is_insecure=is_insecure,
            ),
            name="cURL",
        )


def log_response(
    response: requests.Response,
    needs_allure: bool = True,
) -> None:
    """Log a response and optionally attach it to Allure."""
    elapsed_ms: float = response.elapsed.total_seconds() * 1000
    status_code: int = response.status_code

    color = {
        1: "blue",
        2: "green",
        3: "yellow",
        4: "red",
        5: "red",
    }.get(status_code // 100, "white")

    headers: dict[str, str] = _mask_headers(response.headers)
    content_type: str = _header(response.headers, "Content-Type")
    body_text, _ = _render_body(
        body=response.content,
        content_type=content_type,
    )

    title: str = (
        f"Response: {status_code} {response.reason} "
        f"({elapsed_ms:.0f} ms, {len(response.content)} bytes)"
    )

    message = (
        f"\n<bold><cyan>HTTP RESPONSE</cyan></bold> | "
        f"<{color}><bold>{status_code} {response.reason}</bold></{color}> "
        f"| {elapsed_ms:.0f} ms | {len(response.content)} bytes\n"
        f"<dim>Headers:</dim>"
    )

    for key, value in headers.items():
        message += f"\n  <cyan>{key}</cyan>: {value}"

    if body_text:
        message += f"\n<dim>Body:</dim>\n{body_text}"

    logger.opt(colors=True).debug(message)

    if not needs_allure:
        return

    with allure.step(title):
        _attach(text=_format_headers(headers), name="Response headers")

        if body_text:
            _attach(text=body_text, name="Response body")