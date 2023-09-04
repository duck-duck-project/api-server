import aiohttp
import structlog
from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Update
from structlog.stdlib import BoundLogger

from exceptions import ServerAPIError
from views import (
    ClientConnectorErrorInlineQueryView,
    ServerAPIErrorInlineQueryView,
)

__all__ = ('router',)

logger: BoundLogger = structlog.get_logger('app')

router = Router(name=__name__)


async def on_client_connector_error(
        update: Update,
) -> bool:
    text = '❌ Ошибка подключения к серверу, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    if update.inline_query is not None:
        await update.inline_query.answer([
            ClientConnectorErrorInlineQueryView()
            .get_inline_query_result_article()
        ], is_personal=True)
    await logger.acritical('Can not connect to the API server')
    return True


async def on_server_api_error(
        update: Update,
) -> bool:
    text = '❌ Ошибка API сервера, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    if update.inline_query is not None:
        await update.inline_query.answer([
            ServerAPIErrorInlineQueryView()
            .get_inline_query_result_article()
        ])
    await logger.acritical('Error on the API server side')
    return True


router.errors.register(
    on_client_connector_error,
    ExceptionTypeFilter(aiohttp.ClientConnectorError),
)
router.errors.register(
    on_server_api_error,
    ExceptionTypeFilter(ServerAPIError),
)
