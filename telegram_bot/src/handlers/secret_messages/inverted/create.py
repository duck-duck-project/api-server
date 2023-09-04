from aiogram import F, Router
from aiogram.filters import and_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery

from repositories import HTTPClientFactory

__all__ = ('register_handlers',)


async def on_inverted_secret_message_typing(
        inline_query: InlineQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    text = inline_query.query.lstrip('!')


def register_handlers(router: Router) -> None:
    router.message.register(
        on_inverted_secret_message_typing,
        and_f(F.text, F.text.startswith('!')),
        StateFilter('*'),
    )
