import pytest
from django.urls import reverse
from rest_framework import status
from orders.enums import OrderStatus


@pytest.mark.django_db
class TestOrderCancelView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, pending_order):
        self.url = reverse("orders:customer-cancel", kwargs={"uuid": pending_order.uuid})
        self.client = api_client
        self.user = user
        self.order = pending_order

    def test_cancel_unauthorized_fails(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cancel_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancel_for_paid_order_fails(self, shipped_order):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse("orders:customer-cancel", kwargs={"uuid": shipped_order.uuid}),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_with_valid_data_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.order.refresh_from_db()
        assert self.order.status == OrderStatus.CANCELLED
        self.order.status = OrderStatus.PENDING_PAYMENT
        self.order.save()
