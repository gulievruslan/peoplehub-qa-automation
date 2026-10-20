"""Module contains constants used by all tests."""
from automation.custom.generators.randoms import get_random_string

DEPARTMENT_NAME = "Department created by AT_{random_string}"
FIRST_NAME_RANDOM = "first_name_random_{random_string}"
D_M_Y_DATE = "%d%m%Y"
LEAVE_REQUEST_RANDOM = "leave_request_random_{random_string}"
TESTING_DEPARTMENT = "testing_department"
LEAVE_REQUEST_REASON_RANDOM = f"leaving_request_reason_random_{get_random_string()}"