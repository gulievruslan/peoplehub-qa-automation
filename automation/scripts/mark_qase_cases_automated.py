"""Mark Qase cases linked to Allure results as automated when needed."""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

QASE_API_URL = "https://api.qase.io/v1"


class AllureLabel(TypedDict, total=False):
    """Represent a label stored in an Allure test result."""

    name: str
    value: str


class AllureResult(TypedDict, total=False):
    """Represent the relevant fields from an Allure test result."""

    labels: list[AllureLabel]


class QaseCase(TypedDict, total=False):
    """Represent the automation fields returned for a Qase test case."""

    is_manual: bool
    isManual: bool
    automation: int


class QaseApiResponse(TypedDict, total=False):
    """Represent the relevant fields returned by the Qase API."""

    status: bool
    result: QaseCase


class QaseAutomationUpdate(TypedDict):
    """Represent the payload for marking a Qase case as automated."""

    isManual: bool


@dataclass(frozen=True)
class Arguments:
    """Store command-line arguments for the script.

    Attributes:
        results_dir: Directory containing Allure result JSON files.
    """

    results_dir: Path


def parse_arguments() -> Arguments:
    """Parse command-line arguments.

    Returns:
        Parsed script arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("allure-results"),
        help="Directory containing Allure result JSON files.",
    )
    parsed = parser.parse_args()

    return Arguments(results_dir=parsed.results_dir)


def request_qase(
    method: str,
    url: str,
    token: str,
    payload: QaseAutomationUpdate | None = None,
) -> QaseApiResponse:
    """Send an authenticated request to the Qase API.

    Args:
        method: HTTP method to use.
        url: Qase API endpoint URL.
        token: Qase API token.
        payload: Optional JSON payload for the request.

    Returns:
        Parsed JSON response from the Qase API.

    Raises:
        RuntimeError: If the Qase API returns an unsuccessful response.
    """
    data = json.dumps(payload).encode("utf-8") if payload is not None else None

    request = Request(
        url,
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Token": token,
        },
        method=method,
    )

    try:
        with urlopen(request, timeout=30) as response:
            result = cast(QaseApiResponse, json.loads(response.read().decode("utf-8")))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Qase API {method} request failed: HTTP {error.code}: {details}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Could not reach the Qase API: {error}") from error

    if result.get("status") is False:
        raise RuntimeError(f"Qase API rejected {method} {url}: {result}")

    return result


def collect_qase_ids(results_dir: Path) -> set[int]:
    """Collect Qase case IDs from Allure result files.

    Args:
        results_dir: Directory containing Allure result JSON files.

    Returns:
        Unique Qase case IDs found in the Allure results.
    """
    qase_ids: set[int] = set()

    for result_file in results_dir.glob("*-result.json"):
        with result_file.open(encoding="utf-8") as file:
            result = cast(AllureResult, json.load(file))

        for label in result.get("labels", []):
            if label.get("name") == "qase_id":
                qase_ids.add(int(label["value"]))

    return qase_ids


def is_case_manual(case: QaseCase) -> bool:
    """Determine whether a Qase case is currently marked as manual.

    Args:
        case: Qase test case data returned by the API.

    Returns:
        True if the case is manual; otherwise, False.

    Raises:
        RuntimeError: If the response does not contain a recognized automation field.
    """
    if "is_manual" in case:
        return case["is_manual"]

    if "isManual" in case:
        return case["isManual"]

    # Legacy automation values: 0 = manual, 1 = planned, 2 = automated.
    if "automation" in case:
        return case["automation"] != 2

    raise RuntimeError(
        "Could not determine the case automation status from the Qase API response."
    )


def mark_case_as_automated(project_code: str, case_id: int, token: str):
    """Mark a Qase case as automated if it is currently manual.

    Args:
        project_code: Qase project code.
        case_id: Qase test case ID.
        token: Qase API token.

    Raises:
        HTTPError: If the Qase API returns an unsuccessful HTTP response.
        URLError: If the request cannot reach the Qase API.
        RuntimeError: If the case status cannot be determined or updated.
    """
    encoded_project_code = quote(project_code, safe="")
    case_url = f"{QASE_API_URL}/case/{encoded_project_code}/{case_id}"

    response = request_qase("GET", case_url, token)
    case = response.get("result", response)

    if not is_case_manual(cast(QaseCase, case)):
        print(f"Qase case {case_id} is already automated; skipping.")
        return

    request_qase(
        "PATCH",
        case_url,
        token,
        payload={"isManual": False},
    )
    print(f"Qase case {case_id} marked as automated.")


def main(args: Arguments):
    """Update automation status for cases found in Allure results.

    Args:
        args: Parsed command-line arguments.

    Raises:
        SystemExit: If required configuration or Allure results are missing,
            or if a Qase case cannot be processed.
    """
    token = os.environ.get("QASE_TESTOPS_API_TOKEN")
    project_code = os.environ.get("QASE_PROJECT_CODE")

    if not token or not project_code:
        raise SystemExit("Set QASE_TESTOPS_API_TOKEN and QASE_PROJECT_CODE.")

    if not args.results_dir.is_dir():
        raise SystemExit(f"Allure results directory not found: {args.results_dir}")

    qase_ids = collect_qase_ids(args.results_dir)
    if not qase_ids:
        raise SystemExit("No qase_id labels found in Allure results.")

    print(f"Found {len(qase_ids)} Qase case(s) in Allure results.")

    for case_id in sorted(qase_ids):
        try:
            mark_case_as_automated(project_code, case_id, token)
        except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
            raise SystemExit(f"Failed to process Qase case {case_id}: {error}") from error


if __name__ == "__main__":
    main(parse_arguments())