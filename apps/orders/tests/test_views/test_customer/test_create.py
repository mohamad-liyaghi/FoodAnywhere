import pytest
from django.urls import reverse
from rest_framework import status
from carts.services import CartService


@pytest.mark.django_db
class TestOrderCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        self.url = reverse("orders:customer-list-create")
        self.client = api_client
        self.user = user
        self.data = {}

    def test_create_unauthorized_fails(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_empty_cart_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == ["Cart is empty"]

    def test_create_with_items_succeeds(self, available_drink_product):
        CartService.add_item(self.user, available_drink_product, 2)
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_201_CREATED
