import pytest
from django.urls import reverse
from rest_framework import status
from transactions.models import Transaction
from transactions.enums import TransactionStatus, TransactionType


@pytest.mark.django_db
class TestWithdrawalCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        self.url = reverse("transactions:withdrawal-list-create")
        self.client = api_client
        self.user = user
        self.data = {"amount": 20}

    def test_create_unauthorized_fails(self):
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_user_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_more_than_three_pending_fails(self):
        self.client.force_authenticate(self.user)
        for _ in range(4):
            Transaction.objects.create(
                user=self.user,
                status=TransactionStatus.PENDING,
                amount=20,
                type=TransactionType.WITHDRAWAL,
            )
        response = self.client.post(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You can't create more than 3 pending withdrawals"

    def test_create_with_invalid_data_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_more_than_balance_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {"amount": self.user.balance + 1})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
