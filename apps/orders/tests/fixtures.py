import pytest
from orders.models import Order, OrderItem
from orders.enums import OrderStatus


@pytest.fixture(scope="session")
def pending_order(django_db_setup, django_db_blocker, user, available_food_product) -> Order:
    with django_db_blocker.unblock():
        order = Order.objects.create(
            user=user,
            status=OrderStatus.PENDING_PAYMENT,
            restaurant=available_food_product.restaurant,
        )
        OrderItem.objects.create(
            order=order,
            product=available_food_product,
            quantity=1,
        )
        yield order


@pytest.fixture(scope="session")
def processing_order(django_db_setup, django_db_blocker, user, available_food_product) -> Order:
    with django_db_blocker.unblock():
        order = Order.objects.create(
            user=user,
            status=OrderStatus.PROCESSING,
            restaurant=available_food_product.restaurant,
        )
        OrderItem.objects.create(
            order=order,
            product=available_food_product,
            quantity=1,
        )
        yield order


@pytest.fixture(scope="session")
def shipped_order(django_db_setup, django_db_blocker, user, available_food_product) -> Order:
    with django_db_blocker.unblock():
        order = Order.objects.create(
            user=user,
            status=OrderStatus.SHIPPED,
            restaurant=available_food_product.restaurant,
        )
        OrderItem.objects.create(
            order=order,
            product=available_food_product,
            quantity=1,
        )
        yield order


@pytest.fixture(scope="session")
def delivered_order(django_db_setup, django_db_blocker, user, available_food_product) -> Order:
    with django_db_blocker.unblock():
        order = Order.objects.create(
            user=user,
            status=OrderStatus.DELIVERED,
            restaurant=available_food_product.restaurant,
        )
        OrderItem.objects.create(
            order=order,
            product=available_food_product,
            quantity=1,
        )
        yield order


@pytest.fixture(scope="session")
def cancelled_order(django_db_setup, django_db_blocker, user, available_food_product) -> Order:
    with django_db_blocker.unblock():
        order = Order.objects.create(
            user=user,
            status=OrderStatus.CANCELLED,
            restaurant=available_food_product.restaurant,
        )
        OrderItem.objects.create(
            order=order,
            product=available_food_product,
            quantity=1,
        )
        yield order
