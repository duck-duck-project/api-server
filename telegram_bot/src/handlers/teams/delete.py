from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import TeamDeleteAskForConfirmationCallbackData
from repositories import HTTPClientFactory, TeamRepository
from states import TeamDeleteStates
from views import (
    TeamDeleteAskForConfirmationView,
    edit_message_by_view,
    TeamListView,
)

__all__ = ('register_handlers',)


async def on_team_delete_ask_for_confirmation(
        callback_query: CallbackQuery,
        callback_data: TeamDeleteAskForConfirmationCallbackData,
        state: FSMContext,
) -> None:
    await state.set_state(TeamDeleteStates.confirm)
    await state.update_data(team_id=callback_data.team_id)

    view = TeamDeleteAskForConfirmationView(callback_data.team_id)
    await edit_message_by_view(message=callback_query.message, view=view)


async def on_team_delete_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        team_repository: TeamRepository,
) -> None:
    state_data = await state.get_data()
    await state.clear()
    team_id: int = state_data['team_id']
    user_id = callback_query.from_user.id

    await team_repository.delete_by_id(team_id)
    teams = await team_repository.get_by_user_id(user_id)

    view = TeamListView(teams)
    await edit_message_by_view(message=callback_query.message, view=view)
    await callback_query.answer('🔥 Секретная группа удалена', show_alert=True)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_team_delete_ask_for_confirmation,
        TeamDeleteAskForConfirmationCallbackData.filter(),
        StateFilter('*'),
    )
    router.callback_query.register(
        on_team_delete_confirm,
        StateFilter(TeamDeleteStates.confirm),
    )
