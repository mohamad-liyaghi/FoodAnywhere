import pytest
from django.urls import reverse
from rest_framework import status
from carts.services import CartService


@pytest.mark.django_db
class TestCartListItem:
    @pytest.fixture(autouse=True)
    def setup(self, available_food_product, another_user, api_client):
        self.url = reverse("carts:list-create")
        self.user = another_user
        self.product = available_food_product
        self.quantity = 1
        self.client = api_client

    def test_get_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_empty_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    def test_get_items(self, cart):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
