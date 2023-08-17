from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram.types import Message, ChatType, CallbackQuery

from exceptions import UserDoesNotExistError
from repositories import HTTPClientFactory
from repositories import UserRepository
from services import is_anonymous_messaging_enabled
from views import (
    UserSettingsCalledInGroupChatView,
    UserMenuView,
)
from views import answer_view, edit_message_by_view

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
    await state.finish()
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
    view = UserMenuView(
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
        | CommandStart(deep_link='settings')
        | Text('🔙 Отключить режим анонимных сообщений'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
