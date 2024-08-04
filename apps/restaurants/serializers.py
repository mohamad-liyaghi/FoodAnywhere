from rest_framework import serializers
from restaurants.models import Restaurant
from users.serializers import UserProfileSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "uuid",
            "owner",
            "name",
            "description",
            "phone",
            "location",
            "longitude",
            "latitude",
            "get_status_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uuid",
            "created_at",
            "updated_at",
            "owner",
            "longitude",
            "latitude",
            "get_status_display",
        ]
