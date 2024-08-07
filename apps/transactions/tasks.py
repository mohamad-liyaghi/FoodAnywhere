from celery import shared_task


@shared_task
def do_withdraw(user_id, transaction_id) -> str:
    return f"User {user_id} withdrew {transaction_id}"
