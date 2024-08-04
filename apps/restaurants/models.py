from django.contrib.gis.db import models
from django.conf import settings
from uuid import uuid4
from restaurants.enums import RestaurantStatus


class Restaurant(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurants")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.PointField()
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=RestaurantStatus.choices,
        default=RestaurantStatus.REQUESTED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.longitude = self.location.x
        self.latitude = self.location.y
        super().save(*args, **kwargs)
