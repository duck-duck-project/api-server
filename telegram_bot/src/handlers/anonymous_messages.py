from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ChatType, ContentType
from aiogram.utils.exceptions import TelegramAPIError

from exceptions import UserHasNoPremiumSubscriptionError
from repositories import HTTPClientFactory, UserRepository
from services import (
    determine_media_file_id_and_answer_method,
)
from states import AnonymousMessagingStates
from views import (
    AnonymousMessagingToggledInGroupChatView,
    AnonymousMessagingEnabledView,
    AnonymousMessageSentView,
)
from views import answer_view

__all__ = ('register_handlers',)


async def on_video_note_or_sticker_for_retranslation(
        message: Message,
        chat_id_for_retranslation: int | str,
        bot: Bot,
) -> None:
    method = bot.send_video_note if message.video_note else bot.send_sticker
    try:
        sent_message = await method(
            chat_id_for_retranslation,
            message.video_note.file_id,
        )
    except TelegramAPIError as error:
        text = f'❌ Не получилось отправить\n\nОшибка: {error!s}'
        await message.reply(text)
    else:
        await sent_message.reply('<b>💌 Анонимное сообщение</b>')
        await answer_view(message=message, view=AnonymousMessageSentView())


async def on_media_for_retranslation(
        message: Message,
        chat_id_for_retranslation: int | str,
        bot: Bot,
) -> None:
    media_file_id, method = determine_media_file_id_and_answer_method(
        bot=bot,
        message=message,
    )

    caption = f'<b>💌 Анонимное сообщение</b>'
    if message.caption is not None:
        caption += f'\n\n{message.caption}'

    try:
        await method(
            chat_id_for_retranslation,
            media_file_id,
            caption=caption,
        )
    except TelegramAPIError as error:
        text = f'❌ Не получилось отправить\n\nОшибка: {error!s}'
        await message.reply(text)
    else:
        await answer_view(message=message, view=AnonymousMessageSentView())


async def on_message_for_retranslation(
        message: Message,
        chat_id_for_retranslation: int | str,
        bot: Bot,
) -> None:
    text = f'<b>💌 Анонимное сообщение</b>\n\n{message.html_text}'
    try:
        await bot.send_message(
            chat_id=chat_id_for_retranslation,
            text=text,
        )
    except TelegramAPIError as error:
        text = f'❌ Не получилось отправить\n\nОшибка: {error!s}'
        await message.reply(text)
    else:
        await answer_view(message=message, view=AnonymousMessageSentView())


async def on_toggle_anonymous_messaging_mode_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = AnonymousMessagingToggledInGroupChatView(me.username)
    await answer_view(message=message, view=view)


async def on_toggle_anonymous_messaging_mode(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        user = await user_repository.get_by_id(message.from_user.id)

    if not user.is_premium:
        raise UserHasNoPremiumSubscriptionError(
            '🌟 Анонимные сообщения только для премиум пользователей'
        )
    await AnonymousMessagingStates.enabled.set()
    view = AnonymousMessagingEnabledView()
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_toggle_anonymous_messaging_mode_in_group_chat,
        Command('anonymous_messaging'),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_message_handler(
        on_toggle_anonymous_messaging_mode,
        Command('anonymous_messaging')
        | Text('🔐 Включить анонимные сообщения'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
    dispatcher.register_message_handler(
        on_video_note_or_sticker_for_retranslation,
        content_types=(ContentType.VIDEO_NOTE, ContentType.STICKER),
        chat_type=ChatType.PRIVATE,
        state=AnonymousMessagingStates.enabled,
    )
    dispatcher.register_message_handler(
        on_media_for_retranslation,
        content_types=(
            ContentType.PHOTO,
            ContentType.AUDIO,
            ContentType.VOICE,
            ContentType.ANIMATION,
            ContentType.DOCUMENT,
            ContentType.VIDEO,
        ),
        chat_type=ChatType.PRIVATE,
        state=AnonymousMessagingStates.enabled,
    )
    dispatcher.register_message_handler(
        on_message_for_retranslation,
        content_types=ContentType.TEXT,
        chat_type=ChatType.PRIVATE,
        state=AnonymousMessagingStates.enabled,
    )
