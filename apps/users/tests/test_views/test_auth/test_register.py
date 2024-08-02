import pytest
from django.urls import reverse
from rest_framework import status
from users.tests.utils import generate_user_credentials


@pytest.mark.django_db
class TestUserRegisterView:
    def setup_method(self):
        self.url = reverse("users:register")
        credentials = generate_user_credentials()
        self.data = {
            "email": credentials["email"],
            "password": credentials["password"],
            "first_name": credentials["first_name"],
            "last_name": credentials["last_name"],
        }

    def test_register_with_invalid_data_fails(self, api_client):
        response = api_client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_with_valid_data_succeeds(self, api_client):
        response = api_client.post(self.url, self.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_with_duplicated_data_fails(self, api_client, user):
        self.data["email"] = user.email
        response = api_client.post(self.url, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["email"][0] == "user with this email already exists."
