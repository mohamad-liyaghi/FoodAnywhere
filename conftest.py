import pytest  # noqa
from rest_framework.test import APIClient
from django.core.cache import cache
from config.celery import celery
from apps.users.tests.fixtures import *  # noqa
from apps.active_sessions.tests.fixtures import *  # noqa
from apps.locations.tests.fixtures import *  # noqa
from apps.restaurants.tests.fixtures import *  # noqa
from apps.products.tests.fixtures import *  # noqa
from apps.transactions.tests.fixtures import *  # noqa


@pytest.fixture(scope="class")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(autouse=True, scope="session")
def disable_celery_tasks():
    """
    Disable celery tasks for all tests.
    """
    celery.conf.CELERY_ALWAYS_EAGER = True
    yield
    celery.conf.CELERY_ALWAYS_EAGER = False


@pytest.fixture(autouse=True, scope="class")
def clear_cache():
    """
    Clear cache for all tests.
    """
    cache.clear()
    yield
    cache.clear()
