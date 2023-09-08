from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import ThemeDoesNotExistError
from filters import theme_update_command_filter
from models import User
from repositories import UserRepository
from repositories.themes import ThemeRepository
from views import ThemeSuccessfullyUpdatedView, answer_view

__all__ = ('register_handlers',)


async def on_update_user_theme(
        message: Message,
        user: User,
        user_repository: UserRepository,
        theme_repository: ThemeRepository,
        theme_id: int,
) -> None:
    if not user.is_premium:
        await message.reply(
            '🌟 Смена темы доступна только премиум пользователям'
        )
        return

    theme = await theme_repository.get_by_id(theme_id)

    if theme.is_hidden:
        raise ThemeDoesNotExistError

    await user_repository.update(
        user_id=user.id,
        fullname=user.fullname,
        username=user.username,
        can_be_added_to_contacts=user.can_be_added_to_contacts,
        secret_messages_theme_id=theme_id,
        can_receive_notifications=user.can_receive_notifications,
        born_at=user.born_at,
    )

    view = ThemeSuccessfullyUpdatedView()
    await answer_view(message=message, view=view)


def register_handlers(router: Router) -> None:
    router.message.register(
        on_update_user_theme,
        theme_update_command_filter,
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
