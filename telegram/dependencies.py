from django.conf import settings
from fast_depends import Depends

from telegram.services import (
    TelegramBotContext,
    TelegramBotService,
    TelegramHttpClient,
    closing_telegram_http_client_factory,
)

__all__ = (
    'get_telegram_bot_context',
    'get_telegram_http_client',
    'get_telegram_bot_service',
)


def get_telegram_http_client() -> TelegramHttpClient:
    with closing_telegram_http_client_factory(
            token=settings.TELEGRAM_BOT_TOKEN,
    ) as http_client:
        yield http_client


def get_telegram_bot_service(
        http_client: TelegramHttpClient = Depends(get_telegram_http_client),
) -> TelegramBotService:
    yield TelegramBotService(http_client)


def get_telegram_bot_context(
        telegram_bot_service: TelegramBotService = Depends(
            get_telegram_bot_service,
        ),
) -> TelegramBotContext:
    yield TelegramBotContext(telegram_bot_service)
