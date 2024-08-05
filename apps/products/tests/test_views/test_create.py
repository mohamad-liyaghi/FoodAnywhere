import pytest
from django.urls import reverse
from rest_framework import status
from products.enums import ProductType


@pytest.mark.django_db
class TestLocationCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, approved_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": approved_restaurant.uuid})
        self.client = api_client
        self.data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 10,
            "quantity": 10,
            "max_quantity_per_order": 5,
            "type": ProductType.FOOD,
        }

    def test_create_unauthorized_fails(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_invalid_data_fails(self, user):
        self.client.force_authenticate(user)
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_for_denied_restaurant_fails(self, denied_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": denied_restaurant.uuid})
        self.client.force_authenticate(denied_restaurant.owner)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_for_requested_restaurant_fails(self, request_restaurant):
        self.url = reverse("products:list-create", kwargs={"restaurant_uuid": request_restaurant.uuid})
        self.client.force_authenticate(request_restaurant.owner)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_by_non_owner_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_by_owner_succeeds(self, user):
        self.client.force_authenticate(user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_201_CREATED
