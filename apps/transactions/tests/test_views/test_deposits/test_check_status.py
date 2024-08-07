import pytest
from django.urls import reverse
from rest_framework import status
from transactions.enums import TransactionStatus


@pytest.mark.django_db
class TestDepositCheckStatusView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user, pending_deposit):
        self.url = reverse("transactions:deposit-status-check", kwargs={"uuid": pending_deposit.uuid})
        self.client = api_client
        self.user = user

    def test_retrieve_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_by_non_owner_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_query_param_succeeds(self, pending_deposit, user):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url + "?set_status=ok")
        assert response.status_code == status.HTTP_200_OK
        pending_deposit.refresh_from_db()
        assert pending_deposit.status == TransactionStatus.SUCCESS
        pending_deposit.status = TransactionStatus.PENDING
        pending_deposit.save()
