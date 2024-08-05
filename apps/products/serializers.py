from rest_framework import serializers
from products.models import Product
from restaurants.serializers import RestaurantSerializer


class ProductSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "uuid",
            "name",
            "restaurant",
            "price",
            "quantity",
            "max_quantity_per_order",
            "type",
            "is_available",
        )
        read_only_fields = ("uuid", "is_available")
