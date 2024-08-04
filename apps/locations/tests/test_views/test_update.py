import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLocationUpdateView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, location, api_client):
        self.url = reverse("locations:update", kwargs={"uuid": location.uuid})
        self.client = api_client
        self.user = user
        self.location = location
        self.data = {"title": "Updated Title", "description": "Updated Description"}

    def test_update_unauthorized_fails(self):
        response = self.client.put(self.url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_with_empty_body_fails(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.put(self.url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_succeeds(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_is_primary_succeeds(self, home_location):
        self.client.force_authenticate(self.user)
        url = reverse("locations:update", kwargs={"uuid": home_location.uuid})
        data = {"is_primary": True}
        response = self.client.patch(url, data)
        self.location.refresh_from_db()
        assert self.location.is_primary is False
        assert response.status_code == status.HTTP_200_OK
