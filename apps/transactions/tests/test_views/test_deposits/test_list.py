import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestDepositListView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        self.url = reverse("transactions:deposit-list-create")
        self.client = api_client
        self.user = user

    def test_get_unauthorized_fails(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_by_user_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
