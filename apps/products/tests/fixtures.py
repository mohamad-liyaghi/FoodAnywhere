import pytest
from products.models import Product
from products.enums import ProductType


@pytest.fixture(scope="session")
def available_food_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Available Food Product",
            description="Available Food Product Description",
            price=10.00,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.FOOD,
        )


@pytest.fixture(scope="session")
def unavailable_food_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Unavailable Food Product",
            description="Unavailable Food Product Description",
            price=10.00,
            quantity=0,
            max_quantity_per_order=5,
            type=ProductType.FOOD,
        )


@pytest.fixture(scope="session")
def available_drink_product(django_db_setup, django_db_blocker, another_approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=another_approved_restaurant,
            name="Available Drink Product",
            description="Available Drink Product Description",
            price=5.00,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.DRINK,
        )


@pytest.fixture(scope="session")
def unavailable_drink_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Unavailable Drink Product",
            description="Unavailable Drink Product Description",
            price=5.00,
            quantity=0,
            max_quantity_per_order=5,
            type=ProductType.DRINK,
        )


@pytest.fixture(scope="session")
def available_salad_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Available Salad Product",
            description="Available Salad Product Description",
            price=7.50,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.SALAD,
        )


@pytest.fixture(scope="session")
def unavailable_salad_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Unavailable Salad Product",
            description="Unavailable Salad Product Description",
            price=7.50,
            quantity=0,
            max_quantity_per_order=5,
            type=ProductType.SALAD,
        )


@pytest.fixture(scope="session")
def available_other_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Available Coffee Product",
            description="Available Coffee Product Description",
            price=3.50,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.OTHER,
        )


@pytest.fixture(scope="session")
def unavailable_other_product(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Unavailable Coffee Product",
            description="Unavailable Coffee Product Description",
            price=3.50,
            quantity=0,
            max_quantity_per_order=5,
            type=ProductType.OTHER,
        )


@pytest.fixture(scope="session")
def available_food_to_delete(django_db_setup, django_db_blocker, approved_restaurant) -> Product:
    with django_db_blocker.unblock():
        yield Product.objects.create(
            restaurant=approved_restaurant,
            name="Available Food Product",
            description="Available Food Product Description",
            price=10.00,
            quantity=10,
            max_quantity_per_order=5,
            type=ProductType.FOOD,
        )
