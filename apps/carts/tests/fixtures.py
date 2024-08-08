import pytest
from carts.services import CartService


@pytest.fixture(scope="class")
def cart(user, available_food_product):
    CartService.add_item(user, available_food_product, 1)
    return CartService.get_items(user)
