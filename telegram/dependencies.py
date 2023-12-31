from django.conf import settings

from telegram.services import (
    TelegramBotService,
    closing_telegram_http_client_factory,
)

__all__ = ('get_telegram_bot_service',)


def get_telegram_bot_service() -> TelegramBotService:
    with closing_telegram_http_client_factory(
            token=settings.TELEGRAM_BOT_TOKEN,
    ) as http_client:
        yield TelegramBotService(http_client)
