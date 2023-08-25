from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ChatType

from repositories import TeamRepository, HTTPClientFactory
from views.base import render_message_or_callback_query
from views.teams import TeamListView

__all__ = ('register_handlers',)


async def on_show_teams_list(
        message_or_callback_query: Message | CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    await state.finish()
    user_id = message_or_callback_query.from_user.id

    async with closing_http_client_factory() as http_client:
        team_repository = TeamRepository(http_client)
        teams = await team_repository.get_by_user_id(user_id)

    view = TeamListView(teams)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_teams_list,
        Text('💬 Teams'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_show_teams_list,
        Text('show-teams-list'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
