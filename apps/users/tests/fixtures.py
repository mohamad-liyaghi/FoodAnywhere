import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.tests.utils import generate_user_credentials


@pytest.fixture(scope="session")
def user(django_db_setup, django_db_blocker) -> User:
    with django_db_blocker.unblock():
        yield User.objects.create_user(**generate_user_credentials(), is_active=True, balance=200)


@pytest.fixture(scope="session")
def another_user(django_db_setup, django_db_blocker) -> User:
    with django_db_blocker.unblock():
        yield User.objects.create_user(**generate_user_credentials(), is_active=True, balance=100)


@pytest.fixture(scope="session")
def inactive_user(django_db_setup, django_db_blocker) -> User:
    with django_db_blocker.unblock():
        yield User.objects.create_user(**generate_user_credentials(), is_active=False)


@pytest.fixture(scope="session")
def superuser(django_db_setup, django_db_blocker) -> User:
    with django_db_blocker.unblock():
        yield User.objects.create_superuser(**generate_user_credentials())


@pytest.fixture(scope="session")
def refresh_token(django_db_setup, django_db_blocker, user: User) -> str:
    with django_db_blocker.unblock():
        refresh = RefreshToken.for_user(user)
        return str(refresh)
