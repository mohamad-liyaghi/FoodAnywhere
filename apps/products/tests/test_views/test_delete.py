import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductDeleteView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, approved_restaurant, available_food_to_delete):
        self.url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": available_food_to_delete.restaurant.uuid,
                "product_uuid": available_food_to_delete.uuid,
            },
        )
        self.restaurant = available_food_to_delete.restaurant
        self.product = available_food_to_delete
        self.client = api_client

    def test_delete_unauthorized_fails(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_success(self, user):
        self.client.force_authenticate(user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.product.refresh_from_db()
        assert self.product.is_deleted
