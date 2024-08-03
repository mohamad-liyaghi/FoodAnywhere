import pytest


@pytest.mark.django_db
class TestLocationModel:
    def test_location_str(self, location):
        assert str(location) == location.title

    def test_location_longitude(self, location):
        assert location.longitude == location.location.x

    def test_location_latitude(self, location):
        assert location.latitude == location.location.y
