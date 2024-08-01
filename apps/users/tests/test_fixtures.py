import pytest


@pytest.mark.django_db
def test_user_is_active(user):
    assert user.is_active


@pytest.mark.django_db
def test_inactive_user_is_not_active(inactive_user):
    assert not inactive_user.is_active


@pytest.mark.django_db
def test_user_is_not_staff(user):
    assert not user.is_staff


@pytest.mark.django_db
def test_superuser_level_is_admin(superuser):
    assert superuser.is_superuser
