from django.db import models, transaction
from django.core.cache import cache
from decouple import config
from django.conf import settings
from django.db.models import QuerySet, F
from uuid import uuid4
from orders.exceptions import EmptyCartException
from orders.enums import OrderStatus
from restaurants.models import Restaurant
from products.models import Product


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PENDING_PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_removed_from_balance = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user.email} - {self.restaurant.name} - {self.status}"

    def save(self, *args, **kwargs):
        if self.status == OrderStatus.PROCESSING and not self.is_removed_from_balance:
            self.user.balance -= self.total_price
            self.user.save()
        return super().save(*args, **kwargs)

    @classmethod
    def create_order(cls, user: settings.AUTH_USER_MODEL, cart: dict) -> QuerySet:
        if not cart:
            raise EmptyCartException

        restaurant_ids = set(item["restaurant_id"] for item in cart.values())
        orders = {
            restaurant_id: cls(user=user, restaurant_id=restaurant_id, total_price=0)
            for restaurant_id in restaurant_ids
        }

        # Bulk create Order instances
        Order.objects.bulk_create(orders.values())

        # Prepare for bulk creation of OrderItem instances
        order_items = []
        product_ids = [item["product_id"] for item in cart.values()]
        products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}

        for item in cart.values():
            product = products[item["product_id"]]
            order = orders[item["restaurant_id"]]
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.price,
            )
            order.total_price += order_item.price * order_item.quantity
            order_items.append(order_item)

        with transaction.atomic():
            OrderItem.objects.bulk_create(order_items)
            for order in orders.values():
                order.save()

        # Clear the cache for the user's cart
        cache.delete_many(
            [config("CART_CACHE_KEY").format(user_id=user.id, product_id=product_id) for product_id in product_ids]
        )

        return Order.objects.filter(id__in=[order.id for order in orders.values()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.order.id} - {self.product.name} - {self.quantity}"
