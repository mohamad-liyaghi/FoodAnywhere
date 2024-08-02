import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAccessTokenRefreshView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, refresh_token):
        self.url = reverse("users:refresh-token")
        self.client = api_client
        self.data = {"refresh": refresh_token}

    def test_refresh_with_valid_token(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_refresh_with_invalid_token(self):
        self.data["refresh"] = "invalid refresh"
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data
        assert response.data["detail"] == "Token is invalid or expired"
