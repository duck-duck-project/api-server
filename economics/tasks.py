from celery import shared_task
from django.conf import settings

from economics.services import compute_user_balance, tax_user
from economics.services.allowance import create_allowance
from telegram.services import (
    closing_telegram_http_client_factory,
    TelegramBotService,
    TransactionNotifier,
)
from users.models import User


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
