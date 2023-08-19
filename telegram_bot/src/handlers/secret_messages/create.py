from uuid import UUID

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ChosenInlineResult

from repositories import HTTPClientFactory, SecretMessageRepository
from views import (
    answer_view, SecretMessagePromptView,
    SecretMessageTextMissingInlineQueryView,
)

__all__ = ('register_handlers',)


async def on_show_inline_query_prompt(message: Message) -> None:
    await answer_view(message=message, view=SecretMessagePromptView())


async def on_secret_message_text_missing(inline_query: InlineQuery) -> None:
    items = [
        SecretMessageTextMissingInlineQueryView()
        .get_inline_query_result_article()
    ]
    await inline_query.answer(items, cache_time=1)


async def on_message_created(
        chosen_inline_result: ChosenInlineResult,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
):
    state_data = await state.get_data()

    secret_message_id = UUID(state_data['secret_message_id'])
    text: str = chosen_inline_result.query.lstrip('!')

    if not (0 < len(text) <= 200):
        return

    async with closing_http_client_factory() as http_client:
        secret_message_repository = SecretMessageRepository(http_client)
        await secret_message_repository.create(
            secret_message_id=secret_message_id,
            text=text,
        )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_inline_handler(
        on_secret_message_text_missing,
        Text(''),
        state='*',
    )
    dispatcher.register_message_handler(
        on_show_inline_query_prompt,
        Command('secret_message'),
        state='*',
    )
    dispatcher.register_chosen_inline_handler(
        on_message_created,
        state='*',
    )
