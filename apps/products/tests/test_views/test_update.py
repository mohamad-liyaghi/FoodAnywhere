import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProfileUpdateView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, available_food_product):
        self.url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": available_food_product.restaurant.uuid,
                "product_uuid": available_food_product.uuid,
            },
        )
        self.restaurant = available_food_product.restaurant
        self.product = available_food_product
        self.client = api_client
        self.user = user
        self.data = {"name": "Updated Product"}

    def test_update_unauthorized_fails(self):
        response = self.client.put(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_read_only_field_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, {"uuid": "new-uuid"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_with_empty_body_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_with_valid_data_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.patch(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
