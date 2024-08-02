import pytest
from active_sessions.models import ActiveSession
from active_sessions.enums import LoginDeviceType, LoginBrowserType


@pytest.fixture(scope="session")
def active_session(django_db_setup, django_db_blocker, user) -> ActiveSession:
    with django_db_blocker.unblock():
        yield ActiveSession.objects.create(
            user=user,
            device=LoginDeviceType.ANDROID,
            browser=LoginBrowserType.CHROME,
            ip_address="192.168.1.12",
        )
