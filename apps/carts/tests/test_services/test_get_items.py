import pytest
from carts.services import CartService


@pytest.mark.django_db
class TestCartListItem:
    @pytest.fixture(autouse=True)
    def setup(self, available_food_product, user):
        self.user = user
        self.product = available_food_product
        self.quantity = 1

    def test_get_empty_cart(self):
        items = CartService.get_items(self.user)
        assert items == {}

    def test_get_items(self, cart):
        items = CartService.get_items(self.user)
        assert items[self.product.id]["quantity"] == self.quantity
