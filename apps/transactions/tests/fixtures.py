import pytest
from transactions.models import Transaction
from transactions.enums import TransactionType, TransactionStatus


@pytest.fixture(scope="session")
def successful_deposit(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.SUCCESS,
            is_processed=True,
        )


@pytest.fixture(scope="session")
def failed_deposit(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.FAILED,
        )


@pytest.fixture(scope="session")
def pending_deposit(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
        )


@pytest.fixture(scope="session")
def successful_withdrawal(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.SUCCESS,
            is_processed=True,
        )


@pytest.fixture(scope="session")
def failed_withdrawal(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.FAILED,
        )


@pytest.fixture(scope="session")
def cancelled_withdrawal(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.CANCELLED,
        )


@pytest.fixture(scope="session")
def pending_withdrawal(django_db_setup, django_db_blocker, user) -> Transaction:
    with django_db_blocker.unblock():
        yield Transaction.objects.create(
            user=user,
            amount=100.00,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.PENDING,
        )
