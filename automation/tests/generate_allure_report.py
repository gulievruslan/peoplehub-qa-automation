"""Run tests in parallel and generate the Allure report locally."""

import shutil
import subprocess
import sys
from pathlib import Path

ALLURE_PATH = Path(r"C:\Users\bossd\Desktop\Projects\allure-2.36.0\bin\allure.bat")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALLURE_RESULTS = PROJECT_ROOT / "allure-results"
ALLURE_REPORT = PROJECT_ROOT / "allure-report"

WORKERS = 8


def run_tests() -> bool:
    """Run pytest without retrying failed tests."""
    if ALLURE_RESULTS.exists():
        shutil.rmtree(ALLURE_RESULTS)

    test_path = sys.argv[1] if len(sys.argv) > 1 else "automation/tests"

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "-n",
        str(WORKERS),
        test_path,
        "--tb=short",
        f"--alluredir={ALLURE_RESULTS}",
        "--log-cli-level=INFO",
    ]

    print(f"\nRunning tests: {test_path}")
    print(f"Parallel workers: {WORKERS}")
    print("\nAttempt: 1/1\n")

    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)

    if result.returncode == 0:
        print("\nAll tests passed.")
        return True

    if result.returncode == 1:
        print(
            "\nPytest finished with failed tests or a test collection error. "
            "No automatic retry."
        )
    else:
        print(
            f"\nPytest stopped with exit code {result.returncode}. "
            "No automatic retry."
        )

    return False


def generate_and_open_report() -> None:
    """Generate the Allure report and open it in the default browser."""
    if not ALLURE_RESULTS.exists() or not any(ALLURE_RESULTS.iterdir()):
        print("\nAllure results were not generated. Report will not be opened.")
        return

    if ALLURE_REPORT.exists():
        shutil.rmtree(ALLURE_REPORT)

    print("\nGenerating Allure report...")

    subprocess.run(
        [
            "cmd",
            "/c",
            "call",
            str(ALLURE_PATH),
            "generate",
            str(ALLURE_RESULTS),
            "--clean",
            "-o",
            str(ALLURE_REPORT),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("\nOpening Allure report...")

    subprocess.run(
        [
            "cmd",
            "/c",
            "call",
            str(ALLURE_PATH),
            "open",
            str(ALLURE_REPORT),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


def main() -> int:
    """Run tests, generate the report, and return the test result."""
    try:
        print(f"Script directory: {Path(__file__).resolve().parent}")
        print(f"Project root: {PROJECT_ROOT}")
        print(f"Automation directory exists: {(PROJECT_ROOT / 'automation').is_dir()}")
        tests_passed = run_tests()
        generate_and_open_report()
        return 0 if tests_passed else 1
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"\nError: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())