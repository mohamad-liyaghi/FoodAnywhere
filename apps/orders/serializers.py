from rest_framework import serializers
from carts.services import CartService
from orders.exceptions import EmptyCartException
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

    def create(self, validated_data):
        user = self.context["user"]
        cart = CartService.get_items(user)
        try:
            return Order.create_order(user, cart)
        except EmptyCartException:
            raise serializers.ValidationError("Cart is empty")
