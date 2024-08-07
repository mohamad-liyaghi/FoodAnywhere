from django.utils import timezone
from django.apps import apps
from celery import shared_task
from datetime import timedelta
from transactions.enums import TransactionStatus


@shared_task
def do_withdraw(user_id, transaction_id) -> str:
    return f"User {user_id} withdrew {transaction_id}"


@shared_task
def auto_expire_transactions() -> str:
    Transaction = apps.get_model("transactions", "Transaction")  # noqa
    twenty_minutes_ago = timezone.now() - timedelta(minutes=20)
    transactions = Transaction.objects.filter(
        created_at__lte=twenty_minutes_ago,
        status=TransactionStatus.PENDING,
    ).update(status=TransactionStatus.EXPIRED)
    return f"Expired {transactions} transactions"
