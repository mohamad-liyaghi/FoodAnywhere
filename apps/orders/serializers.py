from rest_framework import serializers
from products.serializers import ProductSerializer
from users.serializers import UserProfileSerializer
from restaurants.serializers import RestaurantSerializer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("user", "restaurant", "get_status_display", "total_price", "items")
        read_only_fields = (
            "user",
            "restaurant",
            "get_status_display",
            "total_price",
            "items",
        )
