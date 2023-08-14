from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatType, Message

from repositories import HTTPClientFactory
from repositories import UserRepository
from services import is_anonymous_messaging_enabled
from views import UserSettingsView, answer_view

__all__ = ('register_handlers',)


async def on_toggle_can_be_added_to_contacts(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        user = await user_repository.get_by_id(message.from_user.id)

        secret_message_theme_id = (
            None if user.secret_message_theme is None
            else user.secret_message_theme.id
        )
        await user_repository.update(
            user_id=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            can_be_added_to_contacts=not user.can_be_added_to_contacts,
            is_premium=user.is_premium,
            secret_messages_theme_id=secret_message_theme_id,
        )
        user = await user_repository.get_by_id(message.from_user.id)
    state_name = await state.get_state()
    view = UserSettingsView(
        user=user,
        is_anonymous_messaging_enabled=is_anonymous_messaging_enabled(
            state_name=state_name,
        )
    )
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_toggle_can_be_added_to_contacts,
        Text('❌ Запретить добавление в контакты')
        | Text('✅ Разрешить добавление в контакты'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
