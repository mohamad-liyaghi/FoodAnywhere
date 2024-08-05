import pytest
from django.core.exceptions import ValidationError
from products.models import Product
from products.enums import ProductType


@pytest.mark.django_db
class TestProductModel:
    def test_product_is_available(self, available_food_product, unavailable_food_product):
        assert available_food_product.is_available
        assert not unavailable_food_product.is_available

    def test_product_clean_method(self, denied_restaurant):
        product = Product(
            restaurant=denied_restaurant,
            name="Test Product",
            description="Test Description",
            price=10.0,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.FOOD,
        )
        with pytest.raises(ValidationError):
            product.save()
