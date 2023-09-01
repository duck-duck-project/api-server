from aiogram import Dispatcher
from aiogram.types import Message, ChatType

from exceptions import ThemeDoesNotExistError
from filters import ThemeUpdateCommandFilter
from models import User
from repositories import HTTPClientFactory, UserRepository
from repositories.themes import ThemeRepository

__all__ = ('register_handlers',)

from views import ThemeSuccessfullyUpdatedView, answer_view


async def on_update_user_theme(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
        user: User,
        theme_id: int,
) -> None:
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        theme_repository = ThemeRepository(http_client)
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


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_update_user_theme,
        ThemeUpdateCommandFilter(),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
