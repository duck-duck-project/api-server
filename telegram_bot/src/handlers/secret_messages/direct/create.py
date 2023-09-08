from uuid import uuid4

from aiogram import Router, F
from aiogram.filters import invert_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle

from models import User
from repositories import ContactRepository, TeamRepository
from services import filter_not_hidden
from views import (
    SecretMessageDetailInlineQueryView,
    TooLongSecretMessageTextInlineQueryView,
    NoUserContactsInlineQueryView,
    NoVisibleContactsInlineQueryView, SecretMessageForTeamInlineQueryView,
)

__all__ = ('register_handlers',)


async def on_secret_message_typing(
        inline_query: InlineQuery,
        contact_repository: ContactRepository,
        team_repository: TeamRepository,
        state: FSMContext,
        user: User,
) -> None:
    text = inline_query.query

    contacts = await contact_repository.get_by_user_id(user.id)
    teams = await team_repository.get_by_user_id(user.id)

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

    teams_and_query_ids = [
        (team, f'{uuid4().hex}@{team.id}')
        for team in teams
    ]
    contacts_and_query_ids = [
        (contact, f'{uuid4().hex}@{contact.id}?')
        for contact in visible_contacts
    ]
    teams_items: list[InlineQueryResultArticle] = [
        SecretMessageForTeamInlineQueryView(
            query_id=query_id,
            team=team,
            secret_message_id=draft_secret_message_id,
        ).get_inline_query_result_article()
        for team, query_id in teams_and_query_ids
    ]
    contacts_items: list[InlineQueryResultArticle] = [
        SecretMessageDetailInlineQueryView(
            query_id=query_id,
            contact=contact,
            secret_message_id=draft_secret_message_id,
            secret_message_theme=user.secret_message_theme,
        ).get_inline_query_result_article()
        for contact, query_id in contacts_and_query_ids
    ]
    items = teams_items + contacts_items
    await inline_query.answer(items, cache_time=1, is_personal=True)


def register_handlers(router: Router) -> None:
    router.inline_query.register(
        on_secret_message_typing,
        F.query,
        invert_f(F.query.startswith('!')),
        StateFilter('*'),
    )
