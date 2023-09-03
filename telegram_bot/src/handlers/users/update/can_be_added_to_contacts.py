from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatType, CallbackQuery

from callback_data import UserUpdateCallbackData
from models import User
from repositories import HTTPClientFactory, UserRepository
from views import edit_message_by_view, UserPersonalSettingsView

__all__ = ('register_handlers',)


async def on_toggle_can_be_added_to_contacts(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
        user: User,
) -> None:
    secret_message_theme_id = None
    if user.secret_message_theme is not None:
        secret_message_theme_id = user.secret_message_theme.id

    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
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


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_toggle_can_be_added_to_contacts,
        UserUpdateCallbackData().filter(field='can_be_added_to_contacts'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
