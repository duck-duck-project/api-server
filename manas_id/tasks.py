import random

from celery import shared_task
from fast_depends import inject, Depends

from economics.dependencies import get_transaction_notifier
from economics.services import create_system_deposit
from manas_id.selectors import iter_manas_ids
from telegram.services import TransactionNotifier


@shared_task
@inject
def give_away_stipends(
        transaction_notifier: TransactionNotifier = Depends(
                get_transaction_notifier,
        )
) -> None:
    for manas_ids in iter_manas_ids():
        for manas_id in manas_ids:
            deposit = create_system_deposit(
                user=manas_id.user,
                amount=random.randint(1000, 5000),
                description='Стипендия'
            )
            transaction_notifier.notify_deposit(deposit)
