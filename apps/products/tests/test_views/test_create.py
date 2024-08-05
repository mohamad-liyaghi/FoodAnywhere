import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductListView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, approved_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": approved_restaurant.uuid})
        self.client = api_client

    def test_retrieve_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_for_denied_restaurant_fails(self, denied_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": denied_restaurant.uuid})
        self.client.force_authenticate(denied_restaurant.owner)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_requested_restaurant_fails(self, request_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": request_restaurant.uuid})
        self.client.force_authenticate(request_restaurant.owner)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_approved_restaurant_succeeds(self, user):
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
