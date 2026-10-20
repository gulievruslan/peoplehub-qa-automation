"""Module contains fixtures for api tests"""
import pytest
from _pytest.fixtures import SubRequest

from automation.api.auth import AuthClient
from automation.config.users import TestUser
from automation.custom.logger.log_fixture import log_fixture
from automation.custom.typed_decorators import typed_title


@pytest.fixture
@log_fixture
@typed_title(value='Authenticate the specified user')
def get_user_token(request: SubRequest) -> str:
    """Authenticate the specified user.

    Args:
        request (SubRequest): pytest fixture
    """
    user: TestUser = request.param

    response = AuthClient().login(email=user.email, password=user.password.get_secret_value())

    response.check_status_code()

    return response.dto().access_token
