import pytest
from django.contrib.gis.geos import Point
from restaurants.models import Restaurant
from restaurants.enums import RestaurantStatus


@pytest.fixture(scope="session")
def request_location(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            user=user,
            name="Request Location",
            description="Request Location Description",
            phone="123456789",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.REQUESTED,
        )


@pytest.fixture(scope="session")
def approved_location(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            user=user,
            name="Approved Location",
            description="Approved Location Description",
            phone="987654321",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.APPROVED,
        )


@pytest.fixture(scope="session")
def denied_location(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            user=user,
            name="Rejected Location",
            description="Rejected Location Description",
            phone="123456789",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.DENIED,
        )


@pytest.fixture(scope="session")
def cancelled_location(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            user=user,
            name="Cancelled Location",
            description="Cancelled Location Description",
            phone="987654321",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.CANCELLED,
        )
