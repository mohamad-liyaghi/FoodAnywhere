from django.db import models


class ProductType(models.TextChoices):
    FOOD = "f", "Food"
    DRINK = "d", "Drink"
    SALAD = "s", "Salad"
    OTHER = "o", "Other"
