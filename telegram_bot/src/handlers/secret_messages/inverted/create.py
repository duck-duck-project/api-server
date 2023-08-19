from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineQuery

from repositories import HTTPClientFactory

__all__ = ('register_handlers',)


async def on_inverted_secret_message_typing(
        inline_query: InlineQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    text = inline_query.query.lstrip('!')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_inline_handler(
        on_inverted_secret_message_typing,
        ~Text(''),
        Text('!'),
        state='*',
    )
