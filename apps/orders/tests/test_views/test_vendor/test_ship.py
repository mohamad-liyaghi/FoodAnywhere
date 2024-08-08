import pytest
from django.urls import reverse
from rest_framework import status
from orders.enums import OrderStatus


@pytest.mark.django_db
class TestOrderShipView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, processing_order):
        self.url = reverse("orders:vendor-shipped", kwargs={"uuid": processing_order.uuid})
        self.client = api_client
        self.user = processing_order.restaurant.owner
        self.order = processing_order
        self.data = {}

    def test_ship_unauthorized_fails(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_ship_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ship_for_paid_order_fails(self, shipped_order):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse("orders:vendor-shipped", kwargs={"uuid": shipped_order.uuid}),
            self.data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_with_valid_data_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK
        self.order.refresh_from_db()
        assert self.order.status == OrderStatus.SHIPPED
        self.order.status = OrderStatus.PROCESSING
        self.order.save()
