from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from callback_data import TeamMemberListCallbackData
from repositories import HTTPClientFactory, TeamMemberRepository
from views import TeamMemberListView, edit_message_by_view

__all__ = ('register_handlers',)


async def on_show_team_members_list(
        callback_query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    await state.finish()
    team_id: int = callback_data['team_id']
    async with closing_http_client_factory() as http_client:
        team_member_repository = TeamMemberRepository(http_client)
        team_members = await team_member_repository.get_by_team_id(team_id)
    view = TeamMemberListView(
        team_members=team_members,
        team_id=team_id,
    )
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_show_team_members_list,
        TeamMemberListCallbackData().filter(),
        state='*',
    )
