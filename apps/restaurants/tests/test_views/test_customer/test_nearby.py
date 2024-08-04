import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestNearbyRestaurantListView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.url = reverse("restaurants:nearby")
        self.client = api_client

    def test_retrieve_list_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_list(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
