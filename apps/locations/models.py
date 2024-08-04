from django.contrib.gis.db import models
from django.conf import settings
from django.db.models import Q
from uuid import uuid4


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="locations")
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    location = models.PointField()
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user}"

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "is_primary"],
                condition=Q(is_primary=True),
                name="unique_primary_location",
            )
        ]

    def save(self, *args, **kwargs):
        self.longitude = self.location.x
        self.latitude = self.location.y
        super().save(*args, **kwargs)
