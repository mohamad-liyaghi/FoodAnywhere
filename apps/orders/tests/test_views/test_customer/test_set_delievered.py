import pytest
from django.urls import reverse
from rest_framework import status
from orders.enums import OrderStatus


@pytest.mark.django_db
class TestOrderDeliverView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, shipped_order):
        self.url = reverse("orders:customer-delivered", kwargs={"uuid": shipped_order.uuid})
        self.client = api_client
        self.user = user
        self.order = shipped_order
        self.data = {}

    def test_set_delivered_unauthorized_fails(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_set_delivered_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_set_delivered_for_paid_order_fails(self, processing_order):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse(
                "orders:customer-delivered",
                kwargs={"uuid": processing_order.uuid},
            ),
            self.data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_with_valid_data_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK
        self.order.refresh_from_db()
        assert self.order.status == OrderStatus.DELIVERED
        self.order.status = OrderStatus.SHIPPED
        self.order.save()
