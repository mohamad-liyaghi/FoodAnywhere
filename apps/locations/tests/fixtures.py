import pytest
from locations.models import Location
from django.contrib.gis.geos import Point


@pytest.fixture(scope="session")
def location(django_db_setup, django_db_blocker, user) -> Location:
    with django_db_blocker.unblock():
        yield Location.objects.create(
            user=user,
            location=Point(-122.4194, 37.7749),
            description="Floor 1 - Room 101",
        )
