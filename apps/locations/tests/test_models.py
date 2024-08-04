import pytest
from django.db.utils import IntegrityError
from locations.models import Location


@pytest.mark.django_db
class TestLocationModel:
    def test_location_str(self, location):
        assert str(location) == f"{location.title} - {location.user}"

    def test_location_longitude(self, location):
        assert location.longitude == location.location.x

    def test_location_latitude(self, location):
        assert location.latitude == location.location.y

    def test_create_two_primary_locations_fails(self, location, user):
        with pytest.raises(IntegrityError):
            Location.objects.create(
                user=user,
                location=location.location,
                description="Floor 2 - Room 202",
                is_primary=True,
            )
