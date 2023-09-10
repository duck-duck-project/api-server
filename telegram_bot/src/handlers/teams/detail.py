from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import TeamDetailCallbackData
from repositories import TeamRepository
from views import edit_message_by_view, TeamDetailView

__all__ = ('register_handlers',)


async def on_show_team_detail(
        callback_query: CallbackQuery,
        callback_data: TeamDetailCallbackData,
        team_repository: TeamRepository,
        state: FSMContext,
        timezone: ZoneInfo,
) -> None:
    await state.clear()
    team = await team_repository.get_by_id(callback_data.team_id)
    view = TeamDetailView(team=team, timezone=timezone)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_team_detail,
        TeamDetailCallbackData.filter(),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
