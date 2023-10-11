from celery import shared_task
from django.conf import settings
from django.db import transaction

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
from telegram.services import (
    closing_telegram_http_client_factory,
    TelegramBotService,
    TransactionNotifier,
    int_gaps,
)
from users.exceptions import UserDoesNotExistsError
from users.models import User
from users.selectors.users import get_user_by_id


@shared_task
def tax_users() -> None:
    users = User.objects.all()

    with closing_telegram_http_client_factory(
            token=settings.TELEGRAM_BOT_TOKEN,
    ) as telegram_http_client:
        telegram_bot_service = TelegramBotService(telegram_http_client)
        transaction_notifier = TransactionNotifier(telegram_bot_service)

        for user in users:
            user_balance = compute_user_balance(user)

            if user_balance < 1000:
                deposit = create_allowance(user=user, balance=user_balance)
                transaction_notifier.notify_deposit(deposit)
            elif user_balance >= 1100:
                withdrawal = tax_user(user=user, balance=user_balance)
                transaction_notifier.notify_withdrawal(withdrawal)


@shared_task
def send_richest_users(
        called_by_user_id: int,
        chat_id: int,
        limit: int,
) -> None:
    try:
        called_by_user = get_user_by_id(called_by_user_id)
    except UserDoesNotExistsError:
        return

    users_balances = get_user_balances()
    richest_users = sort_richest_users(users_balances)

    with transaction.atomic():

        with closing_telegram_http_client_factory(
                token=settings.TELEGRAM_BOT_TOKEN,
        ) as telegram_http_client:
            telegram_bot_service = TelegramBotService(telegram_http_client)
            transaction_notifier = TransactionNotifier(telegram_bot_service)

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
