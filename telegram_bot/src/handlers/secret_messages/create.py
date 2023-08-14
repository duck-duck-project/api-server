import asyncio
from uuid import uuid4, UUID

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    ChosenInlineResult, Message,
)

from repositories import (
    ContactRepository,
    SecretMessageRepository,
    UserRepository,
)
from repositories.base import HTTPClientFactory
from views import (
    SecretMessageDetailInlineQueryView,
    InvertedSecretMessageDetailInlineQueryView,
    EmptySecretMessageTextInlineQueryView,
    NotPremiumUserInlineQueryView,
    TooLongSecretMessageTextInlineQueryView,
    NoUserContactsInlineQueryView,
    answer_view,
    SecretMessagePromptView,
)

__all__ = ('register_handlers',)


async def on_show_inline_query_prompt(message: Message) -> None:
    await answer_view(message=message, view=SecretMessagePromptView())


async def on_whisper_message(
        inline_query: InlineQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    text = inline_query.query

    if not text:
        items = [
            (
                EmptySecretMessageTextInlineQueryView()
                .get_inline_query_result_article()
            )
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        user_repository = UserRepository(http_client)

        async with asyncio.TaskGroup() as task_group:
            user_task = task_group.create_task(
                user_repository.get_by_id(inline_query.from_user.id)
            )
            contacts_task = task_group.create_task(
                contact_repository.get_by_user_id(inline_query.from_user.id)
            )

        user = user_task.result()
        contacts = contacts_task.result()

    if not contacts:
        items = [
            NoUserContactsInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    is_inverted = text.startswith('!')
    if is_inverted:
        items = [
            NotPremiumUserInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    if is_inverted:
        text = text.lstrip('!')
        view_class = InvertedSecretMessageDetailInlineQueryView

    text_length = len(text)
    message_length_limit = 200 if user.is_premium else 90
    if text_length > message_length_limit:
        items = [
            (
                TooLongSecretMessageTextInlineQueryView()
                .get_inline_query_result_article()
            )
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    view_class = SecretMessageDetailInlineQueryView

    draft_secret_message_id = uuid4()
    await state.update_data(
        secret_message_id=draft_secret_message_id.hex,
    )

    contacts_and_query_ids = [
        (contact, uuid4())
        for contact in contacts
        if not contact.is_hidden
    ]

    items: list[InlineQueryResultArticle] = [
        view_class(
            query_id=query_id,
            contact=contact,
            secret_message_id=draft_secret_message_id,
            secret_message_theme=user.secret_message_theme,
        ).get_inline_query_result_article()
        for contact, query_id in contacts_and_query_ids
    ]

    query_id_to_contact_to_user_id = '|'.join(
        f'{query_id.hex}@{contact.to_user.id}'
        for contact, query_id in contacts_and_query_ids
    )
    await state.update_data(contacts=query_id_to_contact_to_user_id)

    await inline_query.answer(items, cache_time=1, is_personal=True)


async def on_message_created(
        chosen_inline_result: ChosenInlineResult,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
        bot: Bot,
):
    state_data = await state.get_data()
    await state.finish()
    contacts: str = state_data['contacts']
    query_ids_and_to_user_ids = [
        query_id_and_to_user_id.split('@')
        for query_id_and_to_user_id in contacts.split('|')
    ]
    query_id_to_user_id = {
        UUID(query_id): int(to_user_id)
        for query_id, to_user_id in query_ids_and_to_user_ids
    }

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

    to_user_id = query_id_to_user_id.get(UUID(chosen_inline_result.result_id))


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_inline_query_prompt,
        Command('secret_message'),
        state='*',
    )
    dispatcher.register_inline_handler(
        on_whisper_message,
        state='*',
    )
    dispatcher.register_chosen_inline_handler(
        on_message_created,
        state='*',
    )
