import pytest
from django.contrib.gis.geos import Point
from restaurants.models import Restaurant
from restaurants.enums import RestaurantStatus


@pytest.fixture(scope="session")
def request_restaurant(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            owner=user,
            name="Request Location",
            description="Request Location Description",
            phone="123456789",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.REQUESTED,
        )


@pytest.fixture(scope="session")
def approved_restaurant(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            owner=user,
            name="Approved Location",
            description="Approved Location Description",
            phone="987654321",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.APPROVED,
        )


@pytest.fixture(scope="session")
def denied_restaurant(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            owner=user,
            name="Rejected Location",
            description="Rejected Location Description",
            phone="123456789",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.DENIED,
        )


@pytest.fixture(scope="session")
def deleted_restaurant(django_db_setup, django_db_blocker, user) -> Restaurant:
    with django_db_blocker.unblock():
        yield Restaurant.objects.create(
            owner=user,
            name="Deleted Location",
            description="Deleted Location Description",
            phone="123456789",
            location=Point(-73.935242, 40.730610),
            status=RestaurantStatus.APPROVED,
            is_soft_deleted=True,
        )
