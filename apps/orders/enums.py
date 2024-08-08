from django.db import models


class OrderStatus(models.TextChoices):
    PENDING_PAYMENT = "pp", "Pending Payment"
    PROCESSING = "pr", "Processing"
    SHIPPED = "sh", "Shipped"
    DELIVERED = "de", "Delivered"
    CANCELLED = "ca", "Cancelled"
