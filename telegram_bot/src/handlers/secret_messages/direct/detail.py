from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import (
    SecretMessageDetailCallbackData,
    SecretMessageForTeamCallbackData,
)
from repositories import (
    ContactRepository,
    SecretMessageRepository,
    TeamMemberRepository,
)
from services import can_see_contact_secret, can_see_team_secret

__all__ = ('register_handlers',)


async def on_show_team_message(
        callback_query: CallbackQuery,
        callback_data: SecretMessageForTeamCallbackData,
        team_member_repository: TeamMemberRepository,
        secret_message_repository: SecretMessageRepository,
) -> None:
    team_members = await team_member_repository.get_by_team_id(
        team_id=callback_data.team_id,
    )
    secret_message = await secret_message_repository.get_by_id(
        secret_message_id=callback_data.secret_message_id,
    )

    if not can_see_team_secret(
            user_id=callback_query.from_user.id,
            team_members=team_members,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)


async def on_show_contact_message(
        callback_query: CallbackQuery,
        callback_data: SecretMessageDetailCallbackData,
        contact_repository: ContactRepository,
        secret_message_repository: SecretMessageRepository,
) -> None:
    contact = await contact_repository.get_by_id(callback_data.contact_id)
    secret_message = await secret_message_repository.get_by_id(
        secret_message_id=callback_data.secret_message_id,
    )

    if not can_see_contact_secret(
            user_id=callback_query.from_user.id,
            contact=contact,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_team_message,
        SecretMessageForTeamCallbackData.filter(),
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_contact_message,
        SecretMessageDetailCallbackData.filter(),
        StateFilter('*'),
    )
