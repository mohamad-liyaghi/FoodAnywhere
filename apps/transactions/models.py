from django.db import models
from django.conf import settings
from decimal import Decimal
from uuid import uuid4
from transactions.enums import TransactionType, TransactionStatus
from transactions.exceptions import InsufficientBalanceError
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
            self._process_transaction()
        super().save(*args, **kwargs)

    def _process_transaction(self):
        amount = Decimal(self.amount)

        if self.type == TransactionType.DEPOSIT:
            self._adjust_balance(amount)
        elif self.type in {TransactionType.WITHDRAWAL, TransactionType.COST}:
            self._adjust_balance(-amount)
        elif self.type == TransactionType.CHARGE:
            self._adjust_balance(amount)

        self.is_processed = True

        if self.type == TransactionType.WITHDRAWAL:
            do_withdraw.delay(self.user.id, self.id)

    def _adjust_balance(self, amount):
        if amount < 0 and self.user.balance < abs(amount):
            raise InsufficientBalanceError
        self.user.balance += amount
        self.user.save()

    @classmethod
    def transfer(cls, sender, receiver, amount) -> tuple:
        """Transfer money from sender to receiver."""
        if sender.balance < amount:
            raise InsufficientBalanceError

        sender_transaction = cls.objects.create(
            user=sender,
            amount=amount,
            type=TransactionType.COST,
            status=TransactionStatus.SUCCESS,
        )
        receiver_transaction = cls.objects.create(
            user=receiver,
            amount=amount,
            type=TransactionType.CHARGE,
            status=TransactionStatus.SUCCESS,
        )
        return sender_transaction, receiver_transaction
