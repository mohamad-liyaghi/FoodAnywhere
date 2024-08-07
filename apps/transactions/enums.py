from django.db import models


class TransactionType(models.TextChoices):
    DEPOSIT = ("d", "Deposit")
    WITHDRAWAL = ("w", "Withdrawal")
    CHARGE = ("c", "Charge")
    COST = ("o", "Cost")


class TransactionStatus(models.TextChoices):
    PENDING = ("p", "Pending")
    SUCCESS = ("s", "Success")
    FAILED = ("f", "Failed")
    CANCELLED = ("c", "Cancelled")
    EXPIRED = ("e", "Expired")
