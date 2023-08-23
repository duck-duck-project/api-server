from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatType

from callback_data import TeamDetailCallbackData
from repositories import HTTPClientFactory, TeamRepository
from views import edit_message_by_view, TeamDetailView

__all__ = ('register_handlers',)


async def on_show_team_detail(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    team_id: int = callback_data['team_id']

    async with closing_http_client_factory() as http_client:
        team_repository = TeamRepository(http_client)
        team = await team_repository.get_by_id(team_id)

    view = TeamDetailView(team)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_show_team_detail,
        TeamDetailCallbackData().filter(),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
