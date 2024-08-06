import pytest
from carts.services import CartService
from carts.exceptions import MaximumQuantityExceeded, ProductNotInCart


@pytest.mark.django_db
class TestCartUpdateItem:
    @pytest.fixture(autouse=True)
    def setup(self, available_food_product, another_user):
        self.user = another_user
        self.product = available_food_product
        self.quantity = 1

    def test_update_item(self):
        CartService.add_item(self.user, self.product, self.quantity)
        updated_quantity = 2
        result = CartService.update_item(self.user, self.product, updated_quantity)
        assert result["quantity"] == updated_quantity

    def test_update_item_with_maximum_quantity(self):
        with pytest.raises(MaximumQuantityExceeded):
            CartService.update_item(self.user, self.product, 100)

    def test_update_item_with_product_not_in_cart(self, available_drink_product):
        with pytest.raises(ProductNotInCart):
            CartService.update_item(self.user, available_drink_product, 1)
