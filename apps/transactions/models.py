from django.db import models
from django.conf import settings
from uuid import uuid4
from transactions.enums import TransactionType, TransactionStatus
from transactions.tasks import do_withdraw


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TransactionType.choices)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.amount} - {self.type} - {self.status}"

    def save(self, *args, **kwargs):
        if self.status == TransactionStatus.SUCCESS and not self.is_processed:
            if self.type == TransactionType.DEPOSIT:
                self._handle_deposit()
            elif self.type == TransactionType.WITHDRAWAL:
                self._handle_withdrawal()
            self.is_processed = True
        return super().save(*args, **kwargs)

    def _handle_deposit(self):
        self.user.balance += self.amount
        self.user.save()

    def _handle_withdrawal(self):
        self.user.balance -= self.amount
        self.user.save()
        do_withdraw.delay(self.user.id, self.id)
