import pytest
from django.db import IntegrityError
from users.models import User
from users.tests.utils import generate_user_credentials


@pytest.mark.django_db
class TestUserModel:
    def test_user_str(self, user):
        assert str(user) == f"{user.email} - {user.first_name} {user.last_name}"

    def test_create_with_existing_email_fails(self, user):
        credentials = generate_user_credentials()
        credentials["email"] = user.email
        with pytest.raises(IntegrityError):
            User.objects.create_user(**credentials)
