import pytest  # noqa
from rest_framework.test import APIClient
from apps.users.tests.fixtures import *  # noqa


@pytest.fixture(scope="class")
def api_client() -> APIClient:
    return APIClient()
