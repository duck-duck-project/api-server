from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram.types import Message, ChatType, CallbackQuery

from models import User
from services import is_anonymous_messaging_enabled
from views import (
    UserSettingsCalledInGroupChatView,
    UserMenuView,
    render_message_or_callback_query,
)
from views import answer_view, edit_message_by_view, UserPersonalSettingsView

__all__ = ('register_handlers',)


async def on_show_personal_settings(
        message_or_callback_query: Message | CallbackQuery,
        user: User,
) -> None:
    view = UserPersonalSettingsView(user)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


async def on_settings_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = UserSettingsCalledInGroupChatView(me.username)
    await answer_view(message=message, view=view)


async def on_show_settings(
        message_or_callback_query: Message | CallbackQuery,
        state: FSMContext,
        user: User,
) -> None:
    await state.finish()
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
        on_show_personal_settings,
        Text('🎨 Персональные настройки'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
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
