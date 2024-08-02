from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from users.managers import UserManager


class User(AbstractUser):
    username = None
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
