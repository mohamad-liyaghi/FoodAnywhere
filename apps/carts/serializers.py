from rest_framework import serializers
from products.models import Product


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(read_only=True)
    product = serializers.SlugRelatedField(
        queryset=Product.objects.filter(is_deleted=False),
        slug_field="uuid",
        write_only=True,
    )
    quantity = serializers.IntegerField(min_value=1, max_value=20)


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=20)
