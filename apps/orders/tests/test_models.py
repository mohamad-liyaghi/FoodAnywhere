import pytest
from django.core.cache import cache
from decouple import config
from orders.models import Order, OrderItem
from orders.enums import OrderStatus
from orders.exceptions import EmptyCartException
from carts.services import CartService


@pytest.mark.django_db
class TestOrderModel:
    def test_create_with_empty_cart_fails(self, user):
        with pytest.raises(EmptyCartException):
            Order.create_order(user, {})

    def test_create_only_one_order(self, user, available_food_product):
        CartService.add_item(user, available_food_product, 1)
        Order.create_order(user, CartService.get_items(user))
        assert Order.objects.filter(user=user, restaurant=available_food_product.restaurant).exists()
        assert not cache.get(config("CART_CACHE_KEY").format(user_id=user.id, product_id=available_food_product.id))

    def test_create_for_two_restaurants(self, user, available_food_product, available_drink_product):
        CartService.add_item(user, available_food_product, 1)
        CartService.add_item(user, available_drink_product, 1)
        orders = Order.create_order(user, CartService.get_items(user))
        assert orders.count() == 2
        assert Order.objects.filter(user=user, restaurant=available_food_product.restaurant).exists()
        assert Order.objects.filter(user=user, restaurant=available_drink_product.restaurant).exists()

    def test_remove_total_from_balance(self, pending_order):
        user_balance = pending_order.user.balance
        pending_order.status = OrderStatus.PROCESSING
        pending_order.save()
        pending_order.user.refresh_from_db()
        assert pending_order.user.balance == user_balance - pending_order.total_price
