from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import TeamDetailCallbackData
from repositories import HTTPClientFactory, TeamRepository
from views import edit_message_by_view, TeamDetailView

__all__ = ('register_handlers',)


async def on_show_team_detail(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
        timezone: ZoneInfo,
) -> None:
    await state.clear()

    team_id: int = callback_data['team_id']

    async with closing_http_client_factory() as http_client:
        team_repository = TeamRepository(http_client)
        team = await team_repository.get_by_id(team_id)

    view = TeamDetailView(team=team, timezone=timezone)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_team_detail,
        TeamDetailCallbackData.filter(),
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
