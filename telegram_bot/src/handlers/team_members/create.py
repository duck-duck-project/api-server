from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import (
    TeamMemberCreateCallbackData,
    TeamMemberCreateAcceptInvitationCallbackData,
)
from repositories import (
    ContactRepository,
    TeamRepository,
    TeamMemberRepository,
)
from states import TeamMemberCreateStates
from views import (
    TeamMemberCreateChooseContactView,
    edit_message_by_view,
    send_view,
)
from views.team_members import TeamMemberCreateAskForConfirmationView

__all__ = ('register_handlers',)


async def on_team_member_invitation_accept(
        callback_query: CallbackQuery,
        callback_data: TeamMemberCreateAcceptInvitationCallbackData,
        team_member_repository: TeamMemberRepository,
) -> None:
    await team_member_repository.create(
        team_id=callback_data.team_id,
        user_id=callback_query.from_user.id,
    )
    await callback_query.answer(
        text='✅ Вы вступили в секретную группу',
        show_alert=True,
    )
    await callback_query.message.delete_reply_markup()


async def on_contact_choice(
        callback_query: CallbackQuery,
        state: FSMContext,
        contact_repository: ContactRepository,
        team_repository: TeamRepository,
        bot: Bot,
) -> None:
    contact_id = int(callback_query.data)
    state_data = await state.get_data()
    team_id: int = state_data['team_id']

    contact = await contact_repository.get_by_id(contact_id)
    team = await team_repository.get_by_id(team_id)

    await state.clear()

    view = TeamMemberCreateAskForConfirmationView(
        from_user=contact.of_user,
        team=team,
    )
    try:
        await send_view(
            bot=bot,
            view=view,
            chat_id=contact.to_user.id,
        )
    except TelegramAPIError:
        await callback_query.answer(
            text='❌ Не удалось отправить приглашение',
            show_alert=True,
        )
    else:
        await callback_query.answer(
            text='✅ Приглашение отправлено',
            show_alert=True,
        )


async def on_start_team_member_creation_flow(
        callback_query: CallbackQuery,
        callback_data: TeamMemberCreateCallbackData,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    user_id = callback_query.from_user.id
    contacts = await contact_repository.get_by_user_id(user_id)

    view = TeamMemberCreateChooseContactView(
        contacts=contacts,
        team_id=callback_data.team_id,
    )
    await state.set_state(TeamMemberCreateStates.contact)
    await state.update_data(team_id=callback_data.team_id)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_team_member_invitation_accept,
        TeamMemberCreateAcceptInvitationCallbackData.filter(),
        StateFilter('*'),
    )
    router.callback_query.register(
        on_contact_choice,
        StateFilter(TeamMemberCreateStates.contact),
    )
    router.callback_query.register(
        on_start_team_member_creation_flow,
        TeamMemberCreateCallbackData.filter(),
        StateFilter('*'),
    )
