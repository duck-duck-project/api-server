from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram.types import Message, ChatType, CallbackQuery

from anonymous_messaging.services import is_anonymous_messaging_enabled
from common.repositories import HTTPClientFactory
from common.views import answer_view, edit_message_by_view
from secret_messaging.exceptions import UserDoesNotExistError
from secret_messaging.repositories import UserRepository
from secret_messaging.views import (
    UserSettingsCalledInGroupChatView,
    UserSettingsView,
)

__all__ = ('register_handlers',)


async def on_settings_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = UserSettingsCalledInGroupChatView(me.username)
    await answer_view(message=message, view=view)


async def on_show_settings(
        message_or_callback_query: Message | CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    from_user = message_or_callback_query.from_user
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        try:
            user = await user_repository.get_by_id(from_user.id)
        except UserDoesNotExistError:
            user = await user_repository.create(
                user_id=from_user.id,
                fullname=from_user.full_name,
                username=from_user.username,
            )

    state_name = await state.get_state()
    view = UserSettingsView(
        user=user,
        is_anonymous_messaging_enabled=is_anonymous_messaging_enabled(
            state_name=state_name,
        )
    )
    if isinstance(message_or_callback_query, Message):
        await answer_view(message=message_or_callback_query, view=view)
    else:
        await edit_message_by_view(
            message=message_or_callback_query.message,
            view=view,
        )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_settings_in_group_chat,
        Command('settings'),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_show_settings,
        Text('show-user-settings'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
    dispatcher.register_message_handler(
        on_show_settings,
        CommandStart()
        | Command('settings')
        | CommandStart(deep_link='settings'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
