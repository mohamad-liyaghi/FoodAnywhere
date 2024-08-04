import pytest
from locations.models import Location


@pytest.mark.django_db
class TestLocationModel:
    def test_location_str(self, location):
        assert str(location) == f"{location.title} - {location.user}"

    def test_location_longitude(self, location):
        assert location.longitude == location.location.x

    def test_location_latitude(self, location):
        assert location.latitude == location.location.y

    def test_set_other_locations_to_not_primary(self, location, user):
        Location.objects.create(
            user=user,
            location=location.location,
            description="Floor 2 - Room 202",
            is_primary=True,
        )
        location.refresh_from_db()
        assert location.is_primary is False
        location.is_primary = True
        location.save()
