from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from models import User
from repositories import UserRepository
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
        user_repository: UserRepository,
) -> None:
    await state.clear()
    state_name = await state.get_state()
    user_balance = await user_repository.get_balance(user_id=user.id)
    view = UserMenuView(
        user=user,
        is_anonymous_messaging_enabled=is_anonymous_messaging_enabled(
            state_name=state_name,
        ),
        balance=user_balance.balance,
    )
    if isinstance(message_or_callback_query, Message):
        await answer_view(message=message_or_callback_query, view=view)
    else:
        await edit_message_by_view(
            message=message_or_callback_query.message,
            view=view,
        )


def register_handlers(router: Router) -> None:
    router.message.register(
        on_show_personal_settings,
        F.text == '🎨 Настройки',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_personal_settings,
        F.data == 'show-personal-settings',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.message.register(
        on_settings_in_group_chat,
        Command('settings'),
        F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_settings,
        F.data == 'show-user-settings',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.message.register(
        on_show_settings,
        or_f(
            F.text.in_({
                '/start',
                '/settings',
                '🔙 Отключить режим анонимных сообщений',
            }),
        ),
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
