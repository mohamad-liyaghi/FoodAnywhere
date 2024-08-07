from rest_framework.permissions import BasePermission
from django.utils import timezone
from datetime import timedelta
from transactions.models import Transaction
from transactions.enums import TransactionStatus, TransactionType


class DepositLimitPermission(BasePermission):
    message = "You can't create more than 3 pending deposits in 20 minutes"

    def has_permission(self, request, view):
        now = timezone.now()
        twenty_minutes_ago = now - timedelta(minutes=20)
        pending_deposits = Transaction.objects.filter(
            user=request.user,
            status=TransactionStatus.PENDING,
            created_at__gte=twenty_minutes_ago,
            type=TransactionType.DEPOSIT,
        ).count()
        return pending_deposits <= 3


class WithdrawalLimitPermission(BasePermission):
    message = "You can't create more than 3 pending withdrawals"

    def has_permission(self, request, view):
        pending_withdrawals = Transaction.objects.filter(
            user=request.user,
            status=TransactionStatus.PENDING,
            type=TransactionType.WITHDRAWAL,
        ).count()
        return pending_withdrawals <= 3
