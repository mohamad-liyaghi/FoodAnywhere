import pytest
from django.urls import reverse
from rest_framework import status
from decouple import config
from carts.services import CartService


@pytest.mark.django_db
class TestCarItemUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, available_food_product, user):
        self.url = reverse("carts:update-delete", kwargs={"product_uuid": available_food_product.uuid})
        self.client = api_client
        self.user = user
        self.product = available_food_product

    def test_update_unauthorized_fails(self):
        response = self.client.put(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_with_maximum_quantity_fails(self):
        self.client.force_authenticate(user=self.user)
        CartService.add_item(self.user, self.product, 1)
        response = self.client.put(
            self.url,
            data={"quantity": 100000},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Maximum quantity exceeded"

    def test_update_with_product_not_in_cart_fails(self, available_drink_product):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(
                "carts:update-delete",
                kwargs={"product_uuid": available_drink_product.uuid},
            ),
            data={"quantity": 1},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_item(self):
        self.client.force_authenticate(user=self.user)
        CartService.add_item(self.user, self.product, 1)
        response = self.client.put(self.url, data={"quantity": 2}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["quantity"] == 2
