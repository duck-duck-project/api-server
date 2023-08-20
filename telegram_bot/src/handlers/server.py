import aiohttp
import structlog
from aiogram import Dispatcher
from aiogram.types import Update
from structlog.stdlib import BoundLogger

from exceptions import ServerAPIError

__all__ = ('register_handlers',)

logger: BoundLogger = structlog.get_logger('app')


async def on_client_connector_error(
        update: Update,
        exception: aiohttp.ClientConnectorError,
) -> bool:
    text = '❌ Ошибка подключения к серверу, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    await logger.acritical(
        'Can not connect to the API server',
        exc_info=exception,
    )
    return True


async def on_server_api_error(
        update: Update,
        exception: ServerAPIError,
) -> bool:
    text = '❌ Ошибка API сервера, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    await logger.acritical(
        'Error on the API server side',
        exc_info=exception,
    )
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_client_connector_error,
        exception=aiohttp.ClientConnectorError,
    )
    dispatcher.register_errors_handler(
        on_server_api_error,
        exception=ServerAPIError,
    )
