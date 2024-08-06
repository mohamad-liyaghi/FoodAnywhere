import pytest
from carts.services import CartService
from carts.exceptions import MaximumQuantityExceeded


@pytest.mark.django_db
class TestCartAddItem:
    @pytest.fixture(autouse=True)
    def setup(self, available_food_product, another_user):
        self.user = another_user
        self.product = available_food_product
        self.quantity = 1

    def test_add_item(self):
        result = CartService.add_item(self.user, self.product, self.quantity)
        assert result == {"is_available": True, "quantity": 1}

    def test_add_item_twice_should_increment_quantity(self):
        result = CartService.add_item(self.user, self.product, self.quantity)
        assert result == {"is_available": True, "quantity": 2}

    def test_add_item_more_than_max_quantity_per_order_fails(self):
        with pytest.raises(MaximumQuantityExceeded):
            CartService.add_item(self.user, self.product, self.product.max_quantity_per_order + 1)
