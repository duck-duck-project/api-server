from uuid import uuid4

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle

from models import User
from repositories import ContactRepository
from services import filter_not_hidden
from views import (
    NoUserContactsInlineQueryView,
    NoVisibleContactsInlineQueryView,
    TooLongSecretMessageTextInlineQueryView,
    InvertedSecretMessageDetailInlineQueryView,
)

__all__ = ('register_handlers',)


async def on_inverted_secret_message_typing(
        inline_query: InlineQuery,
        contact_repository: ContactRepository,
        state: FSMContext,
        user: User,
) -> None:
    text = inline_query.query.lstrip('!')

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
        (contact, f'{uuid4().hex}@{contact.id}?')
        for contact in visible_contacts
    ]
    items: list[InlineQueryResultArticle] = [
        InvertedSecretMessageDetailInlineQueryView(
            query_id=query_id,
            contact=contact,
            secret_message_id=draft_secret_message_id,
            secret_message_theme=user.secret_message_theme,
        ).get_inline_query_result_article()
        for contact, query_id in contacts_and_query_ids
    ]
    await inline_query.answer(items, cache_time=1, is_personal=True)


def register_handlers(router: Router) -> None:
    router.inline_query.register(
        on_inverted_secret_message_typing,
        F.query.startswith('!'),
        StateFilter('*'),
    )
