import pytest
from django.core.cache import cache
from decouple import config
from carts.services import CartService


@pytest.mark.django_db
class TestCartDeleteItem:
    @pytest.fixture(autouse=True)
    def setup(self, available_food_product, another_user):
        self.user = another_user
        self.product = available_food_product
        self.quantity = 1

    def test_delete_item(self):
        CartService.add_item(self.user, self.product, self.quantity)
        CartService.remove_item(self.user, self.product)
        assert not cache.get(config("CART_CACHE_KEY").format(user_id=self.user.id, product_id=self.product.id))
