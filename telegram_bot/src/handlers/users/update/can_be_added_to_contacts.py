from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data import UserUpdateCallbackData
from models import User
from repositories import UserRepository
from views import edit_message_by_view, UserPersonalSettingsView

__all__ = ('register_handlers',)


async def on_toggle_can_be_added_to_contacts(
        callback_query: CallbackQuery,
        state: FSMContext,
        user_repository: UserRepository,
        user: User,
) -> None:
    secret_message_theme_id = None
    if user.secret_message_theme is not None:
        secret_message_theme_id = user.secret_message_theme.id

    await user_repository.update(
        user_id=callback_query.from_user.id,
        fullname=callback_query.from_user.full_name,
        username=callback_query.from_user.username,
        can_be_added_to_contacts=not user.can_be_added_to_contacts,
        secret_messages_theme_id=secret_message_theme_id,
        can_receive_notifications=user.can_receive_notifications,
        born_at=user.born_at,
    )
    user = await user_repository.get_by_id(user.id)

    state_name = await state.get_state()
    view = UserPersonalSettingsView(user)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_toggle_can_be_added_to_contacts,
        UserUpdateCallbackData.filter(F.field == 'can_be_added_to_contacts'),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
