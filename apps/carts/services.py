import json
from decouple import config
from django.core.cache import cache
from users.models import User
from products.models import Product
from carts.exceptions import MaximumQuantityExceeded


class CartService:
    @staticmethod
    def add_item(user: User, product: Product, quantity: int) -> dict:
        """
        Add an item to the user's cart; if it exists, increment
        If it's more than product.max_quantity_per_order raise error
        Items be like: {is_available, quantity}
        """
        if quantity > product.max_quantity_per_order:
            raise MaximumQuantityExceeded
        cache_key = config("CART_CACHE_KEY").format(user_id=user.id, product_id=product.id)
        cart_item = cache.get(cache_key)
        if cart_item:
            cart_item = json.loads(cart_item)
            if cart_item["quantity"] >= product.max_quantity_per_order:
                raise MaximumQuantityExceeded
            cart_item["quantity"] += quantity
        else:
            cart_item = {
                "is_available": product.is_available,
                "quantity": quantity,
                "product_id": product.id,
            }

        cache.set(cache_key, json.dumps(cart_item))
        return cart_item

    @staticmethod
    def get_items(user: User) -> dict:
        """
        Get all items in the user's cart
        """
        cart_items = cache.keys(config("CART_CACHE_KEY").format(user_id=user.id, product_id="*"))
        items = {}
        for item in cart_items:
            item = json.loads(cache.get(item))
            items[item["product_id"]] = item
        return items
