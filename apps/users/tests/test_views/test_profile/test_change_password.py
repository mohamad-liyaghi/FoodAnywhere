import pytest
from django.urls import reverse
from rest_framework import status
from users.tests.utils import generate_user_credentials, BASE_USER_PASSWORD


@pytest.mark.django_db
class TestChangePasswordView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data: dict = generate_user_credentials()
        self.url_path = reverse("users:change_password")
        self.data = {}

    def test_change_password_unauthorized_fails(self, api_client):
        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_change_with_invalid_credentials_fails(self, api_client, user):
        api_client.force_authenticate(user=user)
        self.data["old_password"] = "wrong_password"

        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "wrong_password" != BASE_USER_PASSWORD

    def test_change_with_same_password_fails(self, api_client, user):
        api_client.force_authenticate(user=user)
        self.data["old_password"] = BASE_USER_PASSWORD
        self.data["new_password"] = BASE_USER_PASSWORD

        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_success(self, api_client, user):
        api_client.force_authenticate(user=user)
        self.data["old_password"] = BASE_USER_PASSWORD
        self.data["new_password"] = "new_password"

        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(self.data["new_password"])
