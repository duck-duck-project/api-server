from django.conf import settings
from fast_depends import inject, Depends

from telegram.services import (
    TelegramBotService,
    closing_telegram_http_client_factory, TelegramHttpClient,
)

__all__ = ('get_telegram_bot_service',)


def get_telegram_http_client() -> TelegramHttpClient:
    with closing_telegram_http_client_factory(
            token=settings.TELEGRAM_BOT_TOKEN,
    ) as http_client:
        yield http_client


def get_telegram_bot_service(
        http_client: TelegramHttpClient = Depends(get_telegram_http_client),
) -> TelegramBotService:
    yield TelegramBotService(http_client)
