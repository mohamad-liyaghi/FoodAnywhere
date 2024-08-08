import pytest
from decimal import Decimal
from transactions.models import Transaction
from transactions.enums import TransactionType, TransactionStatus


@pytest.mark.django_db
class TestTransactionModel:
    def test_user_balance_increased_after_successful_deposit(self, user):
        user_balance = user.balance
        successful_deposit = Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.SUCCESS,
        )
        assert user.balance == user_balance + Decimal(successful_deposit.amount)

    def test_user_balance_decreased_after_successful_withdrawal(self, user):
        user_balance = user.balance
        successful_withdrawal = Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.SUCCESS,
        )
        assert user.balance == user_balance - Decimal(successful_withdrawal.amount)
