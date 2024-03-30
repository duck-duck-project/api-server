import random

from django.db import transaction
from fast_depends import Depends, inject

from economics.dependencies import get_transaction_notifier
from economics.models import Transaction
from economics.services.deposit import create_system_deposit
from telegram.services import TransactionNotifier
from users.models import User

__all__ = ('create_allowance', 'create_stipend')


def compute_allowance_amount(balance: int) -> int:
    return int((1000 - balance) * 0.1)


def create_allowance(*, user: User, balance: int) -> Transaction:
    return create_system_deposit(
        user=user,
        amount=compute_allowance_amount(balance),
        description='Пособие по безработице',
    )


@transaction.atomic
@inject
def create_stipend(
        user: User,
        transaction_notifier: TransactionNotifier = Depends(
            get_transaction_notifier,
        )
):
    deposit = create_system_deposit(
        user=user,
        amount=random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5]) * 1440,
        description='Стипендия',
    )
    is_notification_delivered = transaction_notifier.notify_deposit(
        deposit=deposit,
    )
    if not is_notification_delivered:
        transaction.rollback()
        user.is_blocked_bot = True
        user.save()
