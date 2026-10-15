
import allure


QASE_PROJECT_CODE = "PEOPLEHUB"
QASE_CASE_URL = "https://app.qase.io/case/{project_code}-{case_id}"


def pytest_runtest_setup(item):
    qase_marker = item.get_closest_marker("qase_id")
    if qase_marker is None:
        return

    case_id = qase_marker.kwargs.get("id")
    if case_id is None:
        return

    allure.dynamic.link(
        QASE_CASE_URL.format(
            project_code=QASE_PROJECT_CODE,
            case_id=case_id,
        ),
        link_type="test_case",
        name=f"Qase: {QASE_PROJECT_CODE}-{case_id}",
    )
