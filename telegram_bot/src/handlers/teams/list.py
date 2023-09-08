from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from repositories import TeamRepository
from views.base import render_message_or_callback_query
from views.teams import TeamListView

__all__ = ('register_handlers',)


async def on_show_teams_list(
        message_or_callback_query: Message | CallbackQuery,
        team_repository: TeamRepository,
        state: FSMContext,
) -> None:
    await state.clear()
    user_id = message_or_callback_query.from_user.id
    teams = await team_repository.get_by_user_id(user_id)
    view = TeamListView(teams)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


def register_handlers(router: Router) -> None:
    router.message.register(
        on_show_teams_list,
        F.text == '💬 Teams',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_teams_list,
        F.data == 'show-teams-list',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
