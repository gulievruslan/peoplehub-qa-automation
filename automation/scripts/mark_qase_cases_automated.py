"""Mark Qase cases linked to Allure results as automated when needed."""
import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from automation.custom.logger.project_logger import logger

QASE_API_URL = "https://api.qase.io/v1"

type ManualFlag = bool | Literal[0, 1]
type AutomationStatus = Literal[0, 1, 2]


class AllureLabel(TypedDict, total=False):
    """Represent a label stored in an Allure test result."""
    name: str
    value: str


class AllureResult(TypedDict, total=False):
    """Represent the relevant fields from an Allure test result."""
    labels: list[AllureLabel]


class QaseCase(TypedDict, total=False):
    """Represent automation fields returned for a Qase test case."""
    is_manual: ManualFlag
    isManual: ManualFlag
    automation: AutomationStatus


class QaseApiResponse(TypedDict, total=False):
    """Represent relevant fields returned by the Qase API."""
    status: bool
    result: QaseCase


class QaseAutomationUpdate(TypedDict):
    """Represent the payload for marking a Qase case as automated."""
    isManual: Literal[0]


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
        RuntimeError: If the request fails or the API rejects the operation.
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

    except (TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Qase API {method} request failed: {error}") from error

    if result.get("status") is False:
        raise RuntimeError(f"Qase API rejected {method} {url}: {result}")

    return result


def collect_qase_ids(results_dir: Path) -> set[int]:
    """Collect Qase case IDs from Allure result files.

    Args:
        results_dir: Directory containing Allure result JSON files.

    Returns:
        Unique Qase case IDs found in the Allure results.

    Raises:
        RuntimeError: If an Allure result file cannot be read or parsed.
    """
    qase_ids: set[int] = set()

    for result_file in results_dir.glob("*-result.json"):
        try:
            with result_file.open(encoding="utf-8") as file:
                result = cast(AllureResult, json.load(file))

        except (OSError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Could not read Allure result {result_file}: {error}") from error

        for label in result.get("labels", []):
            if label.get("name") == "qase_id":
                try:
                    qase_ids.add(int(label["value"]))

                except (KeyError, ValueError) as error:
                    raise RuntimeError(
                        f"Invalid qase_id label in Allure result {result_file}: {label}"
                    ) from error

    return qase_ids


def is_case_manual(case: QaseCase) -> bool:
    """Determine whether a Qase case is currently marked as manual.

    Args:
        case: Qase test case data returned by the API.

    Returns:
        True if the case is manual; otherwise, False.

    Raises:
        RuntimeError: If the response has no recognized automation field.
    """
    if "is_manual" in case:
        return bool(case["is_manual"])

    if "isManual" in case:
        return bool(case["isManual"])

    if "automation" in case:
        return case["automation"] != 2

    raise RuntimeError(
        f"Could not determine the automation status from the Qase case response: {case}"
    )


def mark_case_as_automated(project_code: str, case_id: int, token: str) -> bool:
    """Mark a Qase case as automated if it is currently manual.

    Args:
        project_code: Qase project code.
        case_id: Qase test case ID.
        token: Qase API token.

    Returns:
        True if the case was updated; otherwise, False.

    Raises:
        RuntimeError: If the API request fails or the case status cannot be determined.
    """
    encoded_project_code = quote(project_code, safe="")
    case_url = f"{QASE_API_URL}/case/{encoded_project_code}/{case_id}"

    response = request_qase("GET", case_url, token)
    case = cast(QaseCase, response.get("result", response))

    if not is_case_manual(case):
        logger.info("Qase case {} is already automated; skipping.", case_id)
        return False

    request_qase(
        method="PATCH",
        url=case_url,
        token=token,
        payload={"isManual": 0},
    )
    logger.info("Marked Qase case {} as automated.", case_id)

    return True


def main(args: Arguments):
    """Update automation status for cases found in Allure results.

    Args:
        args: Parsed command-line arguments.

    Raises:
        SystemExit: If configuration, Allure results, or a Qase API request fails.
    """
    token = os.environ.get("QASE_TESTOPS_API_TOKEN")
    project_code = os.environ.get("QASE_PROJECT_CODE")

    if not token or not project_code:
        logger.error("Set QASE_TESTOPS_API_TOKEN and QASE_PROJECT_CODE.")
        raise SystemExit(1)

    if not args.results_dir.is_dir():
        logger.error("Allure results directory not found: {}", args.results_dir)
        raise SystemExit(1)

    try:
        qase_ids = collect_qase_ids(args.results_dir)

    except RuntimeError as error:

        logger.exception("Failed to collect Qase IDs from Allure results.")

        raise SystemExit(1) from error

    if not qase_ids:
        logger.error("No qase_id labels found in Allure results.")

        raise SystemExit(1)

    logger.info("Found {} Qase case(s) in Allure results.", len(qase_ids))

    updated_count = 0
    skipped_count = 0

    for case_id in sorted(qase_ids):
        try:
            was_updated = mark_case_as_automated(project_code, case_id, token)

        except RuntimeError as error:
            logger.exception("Failed to process Qase case {}.", case_id)
            raise SystemExit(1) from error

        if was_updated:
            updated_count += 1

        else:
            skipped_count += 1

    logger.info(
        "Qase automation status sync completed: {} updated, {} already automated.",
        updated_count,
        skipped_count,
    )


if __name__ == "__main__":
    main(parse_arguments())
