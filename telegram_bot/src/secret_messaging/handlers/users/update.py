from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatType, CallbackQuery

from anonymous_messaging.services import is_anonymous_messaging_enabled
from common.repositories import HTTPClientFactory
from common.views import edit_message_by_view
from secret_messaging.repositories import UserRepository
from secret_messaging.views import UserSettingsView

__all__ = ('register_handlers',)


async def on_toggle_can_be_added_to_contacts(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        user = await user_repository.get_by_id(callback_query.from_user.id)

        secret_message_theme_id = (
            None if user.secret_message_theme is None
            else user.secret_message_theme.id
        )
        await user_repository.update(
            user_id=callback_query.from_user.id,
            fullname=callback_query.from_user.full_name,
            username=callback_query.from_user.username,
            can_be_added_to_contacts=not user.can_be_added_to_contacts,
            is_premium=user.is_premium,
            secret_messages_theme_id=secret_message_theme_id,
        )
        user = await user_repository.get_by_id(callback_query.from_user.id)
    state_name = await state.get_state()
    view = UserSettingsView(
        user=user,
        is_anonymous_messaging_enabled=is_anonymous_messaging_enabled(
            state_name=state_name,
        )
    )
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_toggle_can_be_added_to_contacts,
        Text('toggle_can_be_added_to_contacts'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
