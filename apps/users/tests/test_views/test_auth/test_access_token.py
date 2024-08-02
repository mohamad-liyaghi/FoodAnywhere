import pytest
from django.urls import reverse
from rest_framework import status
from users.tests.utils import BASE_USER_PASSWORD


@pytest.mark.django_db
class TestAccessTokenObtainView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client):
        self.url = reverse("users:access-token")
        self.client = api_client
        self.data = {
            "email": user.email,
            "password": BASE_USER_PASSWORD,
        }

    def test_obtain_with_invalid_password_fails(self):
        response = self.client.post(self.url, data={**self.data, "password": "invalid"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"

    def test_obtain_with_invalid_email_fails(self):
        response = self.client.post(self.url, data={**self.data, "email": "non-existance@gmail.com"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"

    def test_obtain_with_empty_body_fails(self):
        response = self.client.post(self.url, data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_obtain_with_valid_data_succeeds(self):
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
