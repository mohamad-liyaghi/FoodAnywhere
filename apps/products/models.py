from django.db import models
from uuid import uuid4
from products.enums import ProductType
from restaurants.models import Restaurant


class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="products")
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    max_quantity_per_order = models.PositiveIntegerField()
    type = models.CharField(max_length=1, choices=ProductType.choices)

    @property
    def is_available(self):
        return self.quantity > 0

    def __str__(self):
        return self.name
