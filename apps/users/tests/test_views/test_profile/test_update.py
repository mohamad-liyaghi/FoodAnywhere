import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProfileUpdateView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client):
        self.url = reverse("users:profile")
        self.client = api_client
        self.user = user
        self.data = {"last_name": "Doe"}

    def test_update_unauthorized_fails(self):
        response = self.client.put(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_read_only_field_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, {"email": "updated@gmail.com"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_with_empty_body_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_with_valid_data_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["last_name"] == self.data["last_name"]
        self.user.refresh_from_db()
        assert self.user.last_name == self.data["last_name"]
