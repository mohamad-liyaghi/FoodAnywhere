import pytest
from django.urls import reverse
from rest_framework import status
from uuid import uuid4


@pytest.mark.django_db
class TestRetrieveProductView:
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

    def test_retrieve_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_invalid_product_fails(self, user, api_client):
        url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": self.restaurant.uuid,
                "product_uuid": uuid4(),
            },
        )
        api_client.force_authenticate(user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_invalid_restaurant_fails(self, user, api_client, available_food_product):
        url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": uuid4(),
                "product_uuid": available_food_product.uuid,
            },
        )
        api_client.force_authenticate(user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_denied_restaurant_fails(self, denied_restaurant):
        url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": denied_restaurant.uuid,
                "product_uuid": self.product.uuid,
            },
        )
        self.client.force_authenticate(denied_restaurant.owner)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_requested_restaurant_fails(self, request_restaurant, available_food_product):
        url = reverse(
            "products:detail",
            kwargs={
                "restaurant_uuid": request_restaurant.uuid,
                "product_uuid": available_food_product.uuid,
            },
        )
        self.client.force_authenticate(request_restaurant.owner)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_for_approved_restaurant_succeeds(self, user, available_food_product):
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
