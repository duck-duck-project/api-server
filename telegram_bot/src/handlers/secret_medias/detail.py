import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, ChatType
from aiogram.utils.exceptions import TelegramAPIError

from models import SecretMediaType
from repositories import HTTPClientFactory
from repositories import SecretMediaRepository
from services import (
    can_see_contact_secret,
    extract_secret_media_id,
    get_message_method_by_media_type,
)
from views import SecretMediaDetailView

__all__ = ('register_handlers',)


async def on_show_secret_media(
        message: Message,
        deep_link: re.Match,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    secret_media_id = extract_secret_media_id(deep_link.string)
    async with closing_http_client_factory() as http_client:
        secret_media_repository = SecretMediaRepository(http_client)
        secret_media = await secret_media_repository.get_by_id(
            secret_media_id=secret_media_id,
        )

    if not can_see_contact_secret(
            user_id=message.from_user.id,
            contact=secret_media.contact,
    ):
        await message.reply('Это секретное медиа не предназначено для вас')
        return

    view = SecretMediaDetailView(secret_media)

    message_method = get_message_method_by_media_type(
        message=message,
        media_type=secret_media.media_type,
    )

    try:
        if secret_media.media_type in (
                SecretMediaType.VIDEO_NOTE,
                SecretMediaType.STICKER,
        ):
            sent_message = await message_method(secret_media.file_id)
            await sent_message.reply(text=view.get_text())
        else:
            await message_method(secret_media.file_id, caption=view.get_text())
    except TelegramAPIError:
        await message.answer('❌ Не удалось загрузить секретное медиа')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_secret_media,
        CommandStart(deep_link=re.compile(r'^secret_media-[0-9a-fA-F]{32}$')),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
