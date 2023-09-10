from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from repositories import TeamRepository
from states import TeamCreateStates
from views import (
    TeamDetailView,
    answer_view,
    TeamCreateAskForNameView,
    edit_message_by_view,
)

__all__ = ('register_handlers',)


async def on_start_team_creation_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(TeamCreateStates.name)
    view = TeamCreateAskForNameView()
    await edit_message_by_view(message=callback_query.message, view=view)


async def on_team_name_input(
        message: Message,
        state: FSMContext,
        timezone: ZoneInfo,
        team_repository: TeamRepository,
) -> None:
    name = message.text
    if len(name) > 64:
        await message.reply('❌ Слишком длинное название')
        return

    team = await team_repository.create(
        user_id=message.from_user.id,
        name=name,
    )

    await state.clear()
    await message.answer('✅ Секретная группа создана')

    view = TeamDetailView(team=team, timezone=timezone)
    await answer_view(message=message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_start_team_creation_flow,
        F.data == 'create-team',
        StateFilter('*'),
    )
    router.message.register(
        on_team_name_input,
        F.text,
        F.chat.type == ChatType.PRIVATE,
        StateFilter(TeamCreateStates.name),
    )
