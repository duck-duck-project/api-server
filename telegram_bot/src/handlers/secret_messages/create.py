from uuid import uuid4, UUID

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    ChosenInlineResult, Message,
)

from models import User
from repositories import (
    ContactRepository,
    SecretMessageRepository,
)
from repositories.base import HTTPClientFactory
from services import filter_not_hidden
from views import (
    SecretMessageDetailInlineQueryView,
    SecretMessageTextMissingInlineQueryView,
    TooLongSecretMessageTextInlineQueryView,
    NoUserContactsInlineQueryView,
    answer_view,
    SecretMessagePromptView,
    NoVisibleContactsInlineQueryView,
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


async def on_inverted_secret_message_typing(
        inline_query: InlineQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    text = inline_query.query.lstrip('!')


async def on_secret_message_typing(
        inline_query: InlineQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
        user: User,
) -> None:
    text = inline_query.query

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contacts = await contact_repository.get_by_user_id(user.id)

    if not contacts:
        items = [
            NoUserContactsInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    visible_contacts = filter_not_hidden(contacts)

    if not visible_contacts:
        items = [
            NoVisibleContactsInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    message_length_limit = 200 if user.is_premium else 60
    if len(text) > message_length_limit:
        items = [
            TooLongSecretMessageTextInlineQueryView()
            .get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    draft_secret_message_id = uuid4()
    await state.update_data(secret_message_id=draft_secret_message_id.hex)

    contacts_and_query_ids = [
        (contact, f'{uuid4().hex}@{contact.to_user.id}')
        for contact in visible_contacts
    ]

    items: list[InlineQueryResultArticle] = [
        SecretMessageDetailInlineQueryView(
            query_id=query_id,
            contact=contact,
            secret_message_id=draft_secret_message_id,
            secret_message_theme=user.secret_message_theme,
        ).get_inline_query_result_article()
        for contact, query_id in contacts_and_query_ids
    ]
    await inline_query.answer(items, cache_time=1, is_personal=True)


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
    dispatcher.register_inline_handler(
        on_inverted_secret_message_typing,
        ~Text(''),
        Text('!'),
        state='*',
    )
    dispatcher.register_inline_handler(
        on_secret_message_typing,
        ~Text(''),
        ~Text('!'),
        state='*',
    )
    dispatcher.register_chosen_inline_handler(
        on_message_created,
        state='*',
    )
