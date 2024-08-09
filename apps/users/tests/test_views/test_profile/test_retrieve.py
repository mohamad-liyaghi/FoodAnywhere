import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal


@pytest.mark.django_db
class TestProfileRetrieveView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client):
        self.url = reverse("users:profile")
        self.client = api_client

    def test_retrieve_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authorized_succeeds(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
