from celery import shared_task
from django.db import transaction
from fast_depends import Depends, inject

from economics.dependencies import get_transaction_notifier
from economics.exceptions import InsufficientFundsForSystemWithdrawalError
from economics.models import OperationPrice
from economics.services import (
    compute_user_balance,
    tax_user,
    create_system_withdrawal,
    get_user_balances,
    sort_richest_users,
)
from economics.services.allowance import create_allowance
from telegram.dependencies import get_telegram_bot_service
from telegram.services import (
    TransactionNotifier,
    int_gaps, TelegramBotService,
)
from users.exceptions import UserDoesNotExistsError
from users.models import User
from users.selectors.users import get_user_by_id


@shared_task
@inject
def tax_users(
        transaction_notifier: TransactionNotifier = (
                Depends(get_transaction_notifier)
        ),
) -> None:
    users = User.objects.all()

    for user in users:
        user_balance = compute_user_balance(user)

        if user_balance < 1000:
            deposit = create_allowance(user=user, balance=user_balance)
            transaction_notifier.notify_deposit(deposit)
        elif user_balance >= 1100:
            withdrawal = tax_user(user=user, balance=user_balance)
            transaction_notifier.notify_withdrawal(withdrawal)


@shared_task
@inject
def send_richest_users(
        called_by_user_id: int,
        chat_id: int,
        limit: int,
        telegram_bot_service: TelegramBotService = (
                Depends(get_telegram_bot_service)
        ),
        transaction_notifier: TransactionNotifier = (
                Depends(get_transaction_notifier)
        ),
) -> None:
    try:
        called_by_user = get_user_by_id(called_by_user_id)
    except UserDoesNotExistsError:
        return

    users_balances = get_user_balances()
    richest_users = sort_richest_users(users_balances)[:limit]

    with transaction.atomic():

        try:
            withdrawal = create_system_withdrawal(
                amount=OperationPrice.RICHEST_USERS,
                description='Просмотр статистики по самым богатым пользователям',
                user=called_by_user,
            )
        except InsufficientFundsForSystemWithdrawalError:
            transaction_notifier.notify_insufficient_funds(chat_id)
            return

        transaction_notifier.notify_withdrawal(withdrawal)

        text = ['Самые богатые пользователи:']

        for i, user in enumerate(richest_users, start=1):
            name = user.user_username or user.user_fullname
            text.append(f'{i}. {name} - {int_gaps(user.balance)}')

        telegram_bot_service.send_message(
            chat_id=chat_id,
            text='\n'.join(text),
        )
