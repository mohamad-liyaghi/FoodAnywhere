from django.db import models


class TransactionType(models.TextChoices):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    REFUND = "refund"


class TransactionStatus(models.TextChoices):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
