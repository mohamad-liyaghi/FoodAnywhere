import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal


@pytest.mark.django_db
class TestRestaurantRetrieveView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, approved_restaurant):
        self.url = reverse("restaurants:vendor-detail", kwargs={"uuid": approved_restaurant.uuid})
        self.client = api_client

    def test_retrieve_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authorized_succeeds(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_requested_restaurant_fails(self, user, request_restaurant):
        self.client.force_authenticate(user=user)
        url = reverse("restaurants:vendor-detail", kwargs={"uuid": request_restaurant.uuid})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_denied_restaurant_fails(self, user, denied_restaurant):
        self.client.force_authenticate(user=user)
        url = reverse("restaurants:vendor-detail", kwargs={"uuid": denied_restaurant.uuid})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
