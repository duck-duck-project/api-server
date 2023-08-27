from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from callback_data import TeamMemberDeleteCallbackData
from repositories import HTTPClientFactory, TeamMemberRepository

__all__ = ('register_handlers',)


async def on_delete_team_member(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    team_member_id: int = callback_data['team_member_id']

    async with closing_http_client_factory() as http_client:
        team_member_repository = TeamMemberRepository(http_client)
        await team_member_repository.delete_by_id(team_member_id)

    await callback_query.answer('✅ Участник удален', show_alert=True)
    await callback_query.message.delete_reply_markup()


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_delete_team_member,
        TeamMemberDeleteCallbackData().filter(),
        state='*',
    )
