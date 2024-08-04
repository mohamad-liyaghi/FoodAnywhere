import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRestaurantRetrieveView:
    @pytest.fixture(autouse=True)
    def setup_method(self, user, api_client, approved_restaurant):
        self.url = reverse("restaurants:vendor-detail", kwargs={"uuid": approved_restaurant.uuid})
        self.client = api_client

    def test_delete_unauthorized_fails(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_another_user_fails(self, another_user):
        self.client.force_authenticate(another_user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_already_deleted_fails(self, deleted_restaurant):
        self.client.force_authenticate(deleted_restaurant.owner)
        url = reverse("restaurants:vendor-detail", kwargs={"uuid": deleted_restaurant.uuid})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_approved_restaurant_succeeds(self, approved_restaurant):
        self.client.force_authenticate(approved_restaurant.owner)
        url = reverse("restaurants:vendor-detail", kwargs={"uuid": approved_restaurant.uuid})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        approved_restaurant.refresh_from_db()
        assert approved_restaurant.is_soft_deleted is True
        approved_restaurant.is_soft_deleted = False
        approved_restaurant.save()

    def test_delete_requested_restaurant_succeeds(self, request_restaurant):
        self.client.force_authenticate(request_restaurant.owner)
        url = reverse("restaurants:vendor-detail", kwargs={"uuid": request_restaurant.uuid})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        request_restaurant.refresh_from_db()
        assert request_restaurant.is_soft_deleted is True
        request_restaurant.is_soft_deleted = False
        request_restaurant.save()
