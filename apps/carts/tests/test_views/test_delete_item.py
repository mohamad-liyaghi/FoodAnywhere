import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from decouple import config
from carts.services import CartService


@pytest.mark.django_db
class TestCarDeleteItemView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, available_food_product, user):
        self.url = reverse("carts:update-delete", kwargs={"product_uuid": available_food_product.uuid})
        self.client = api_client
        self.user = user
        self.product = available_food_product

    def test_delete_unauthorized_fails(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_item(self):
        CartService.add_item(self.user, self.product, 1)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not cache.get(config("CART_CACHE_KEY").format(user_id=self.user.id, product_id=self.product.id))

    def test_delete_deleted_product_fails(self, available_food_to_delete):
        url = reverse(
            "carts:update-delete",
            kwargs={"product_uuid": available_food_to_delete.uuid},
        )
        available_food_to_delete.is_deleted = True
        available_food_to_delete.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert available_food_to_delete.is_deleted
