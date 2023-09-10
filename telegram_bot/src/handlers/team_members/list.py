from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import TeamMemberListCallbackData
from repositories import TeamMemberRepository
from views import TeamMemberListView, edit_message_by_view

__all__ = ('register_handlers',)


async def on_show_team_members_list(
        callback_query: CallbackQuery,
        callback_data: TeamMemberListCallbackData,
        state: FSMContext,
        team_member_repository: TeamMemberRepository,
) -> None:
    await state.clear()
    team_members = await team_member_repository.get_by_team_id(
        team_id=callback_data.team_id,
    )
    view = TeamMemberListView(
        team_members=team_members,
        team_id=callback_data.team_id,
        current_user_id=callback_query.from_user.id,
    )
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_team_members_list,
        TeamMemberListCallbackData.filter(),
        StateFilter('*'),
    )
