from rest_framework import serializers
from locations.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "uuid",
            "title",
            "location",
            "longitude",
            "latitude",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "longitude", "latitude", "created_at", "updated_at"]
