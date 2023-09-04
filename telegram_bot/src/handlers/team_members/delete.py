from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import TeamMemberDeleteCallbackData
from repositories import HTTPClientFactory, TeamMemberRepository

__all__ = ('register_handlers',)


async def on_delete_team_member(
        callback_query: CallbackQuery,
        callback_data: TeamMemberDeleteCallbackData,
        closing_http_client_factory: HTTPClientFactory,
) -> None:

    async with closing_http_client_factory() as http_client:
        team_member_repository = TeamMemberRepository(http_client)
        await team_member_repository.delete_by_id(
            team_member_id=callback_data.team_member_id,
        )

    await callback_query.answer('✅ Участник удален', show_alert=True)
    await callback_query.message.delete_reply_markup()


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_delete_team_member,
        TeamMemberDeleteCallbackData.filter(),
        StateFilter('*'),
    )