from django.db import models
from django.conf import settings
from uuid import uuid4
from transactions.enums import TransactionType, TransactionStatus


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_added_to_balance = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.amount} - {self.type} - {self.status}"
