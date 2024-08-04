import pytest
import json
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestVenorRestaturantCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.url = reverse("restaurants:vendor-list-create")
        self.client = api_client
        self.data = {
            "location": json.dumps({"type": "Point", "coordinates": [-122.4194, 37.7749]}),
            "name": "Test Restaurant",
            "description": "Test Description",
            "phone": "1234567890",
        }

    def test_create_unauthorized_fails(self):
        response = self.client.post(self.url, data=self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_invalid_data_fails(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_valid_data_succeeds(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data=self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == self.data["name"]
