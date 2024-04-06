import contextlib
import json
from typing import NewType

import httpx

from economics.models import OperationPrice, Transaction
from users.models import User

__all__ = (
    'TelegramHttpClient',
    'closing_telegram_http_client_factory',
    'TelegramBotService',
    'TransactionNotifier',
    'TelegramBotContext',
    'int_gaps',
)

TelegramHttpClient = NewType('TelegramHttpClient', httpx.Client)


@contextlib.contextmanager
def closing_telegram_http_client_factory(
        token: str,
) -> TelegramHttpClient:
    base_url = f'https://api.telegram.org/bot{token}/'
    with httpx.Client(base_url=base_url) as http_client:
        yield http_client


class TelegramBotService:

    def __init__(self, telegram_http_client: TelegramHttpClient):
        self.__telegram_http_client = telegram_http_client

    def send_message(self, chat_id: int | str, text: str) -> bool:
        request_data = {
            'chat_id': chat_id,
            'text': text,
        }
        url = '/sendMessage'
        try:
            response = self.__telegram_http_client.post(url, json=request_data)
        except httpx.HTTPError:
            return False
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            return False
        return response_data.get('ok', False)


class TransactionNotifier:

    def __init__(self, telegram_bot_service: TelegramBotService):
        self.__telegram_bot_service = telegram_bot_service

    def notify_withdrawal(self, withdrawal: Transaction) -> None:
        text = f'🔥 Списание на сумму {withdrawal.amount} дак-дак коинов\n'

        if withdrawal.description is not None:
            text += f'ℹ {withdrawal.description}'

        self.__telegram_bot_service.send_message(
            chat_id=withdrawal.sender.id,
            text=text,
        )

    def notify_deposit(self, deposit: Transaction) -> bool:
        text = f'✅ Пополнение на сумму {deposit.amount} дак-дак коинов\n'

        if deposit.description is not None:
            text += f'ℹ {deposit.description}'

        return self.__telegram_bot_service.send_message(
            chat_id=deposit.recipient.id,
            text=text,
        )

    def notify_insufficient_funds(self, chat_id: int) -> None:
        text = (
            '❌ Недостаточно средств на балансе.\n'
            f'Необходимо {OperationPrice.RICHEST_USERS} дак-дак коинов'
        )

        self.__telegram_bot_service.send_message(
            chat_id=chat_id,
            text=text,
        )


class TelegramBotContext:

    def __init__(self, telegram_bot_service: TelegramBotService):
        self.__telegram_bot_service = telegram_bot_service

    def send_if_not_blocked(self, *, user: User, text: str) -> bool:
        if user.is_blocked_bot:
            return False

        return self.__telegram_bot_service.send_message(
            chat_id=user.id,
            text=text,
        )


def int_gaps(number: int) -> str:
    return f'{number:,}'.replace(',', ' ')
