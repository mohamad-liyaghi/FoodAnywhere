from django.db import models


class RestaurantStatus(models.TextChoices):
    REQUESTED = "r", "Requested"
    APPROVED = "a", "Approved"
    DENIED = "d", "Denied"
