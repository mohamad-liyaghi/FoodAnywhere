import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCartAddItemView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, available_food_product, user):
        self.url = reverse("carts:list-create")
        self.client = api_client
        self.user = user
        self.product = available_food_product
        self.data = {
            "product": available_food_product.uuid,
            "quantity": 1,
        }

    def test_add_unauthorized_fails(self):
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def add_item_authorized_succeeds(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {"is_available": True, "quantity": 1}

    def test_item_item_twice_should_increment_quantity(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_item_more_than_max_quantity_per_order_fails(self):
        self.client.force_authenticate(user=self.user)
        self.data["quantity"] = self.product.max_quantity_per_order + 1
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Maximum quantity exceeded"}

    def test_add_deleted_product_fails(self, available_food_to_delete):
        available_food_to_delete.is_deleted = True
        available_food_to_delete.save()
        self.client.force_authenticate(user=self.user)
        self.data["product"] = available_food_to_delete.uuid
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
