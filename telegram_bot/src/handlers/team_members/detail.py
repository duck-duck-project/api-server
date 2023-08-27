from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from callback_data import TeamMemberDetailCallbackData
from repositories import HTTPClientFactory, TeamMemberRepository
from views import TeamMemberMenuDetailView, edit_message_by_view

__all__ = ('register_handlers',)


async def on_show_team_member_menu(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        team_member_repository = TeamMemberRepository(http_client)
        team_member = await team_member_repository.get_by_id(
            team_member_id=callback_data['team_member_id'],
        )
    view = TeamMemberMenuDetailView(team_member)
    await edit_message_by_view(
        view=view,
        message=callback_query.message,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_show_team_member_menu,
        TeamMemberDetailCallbackData().filter(),
        state='*',
    )
