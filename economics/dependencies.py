from fast_depends import Depends, inject

from telegram.dependencies import get_telegram_bot_service
from telegram.services import TransactionNotifier, TelegramBotService

__all__ = ('get_transaction_notifier',)


def get_transaction_notifier(
        telegram_bot_service: TelegramBotService = (
                Depends(get_telegram_bot_service)
        ),
) -> TransactionNotifier:
    return TransactionNotifier(telegram_bot_service)
