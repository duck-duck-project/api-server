from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ChatType, CallbackQuery, ContentType
from aiogram.utils.exceptions import TelegramAPIError

from services import (
    is_anonymous_messaging_enabled,
    determine_media_file_id_and_answer_method,
)
from states import AnonymousMessagingStates
from views import (
    AnonymousMessagingToggledInGroupChatView,
    AnonymousMessagingDisabledView,
    AnonymousMessagingEnabledView,
)
from views import answer_view, edit_message_by_view

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
        await message.reply('✅ Отправлено')


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
        await message.reply('✅ Отправлено')


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
        await message.reply('✅ Отправлено')


async def on_toggle_anonymous_messaging_mode_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = AnonymousMessagingToggledInGroupChatView(me.username)
    await answer_view(message=message, view=view)


async def on_toggle_anonymous_messaging_mode(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await callback_query.answer(
        text='Анонимные сообщения временно отключены',
        show_alert=True,
    )
    return
    state_name = await state.get_state()

    if is_anonymous_messaging_enabled(state_name):
        await state.finish()
        view = AnonymousMessagingDisabledView()
    else:
        await AnonymousMessagingStates.enabled.set()
        view = AnonymousMessagingEnabledView()

    await edit_message_by_view(
        message=callback_query.message,
        view=view,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_toggle_anonymous_messaging_mode_in_group_chat,
        Command('anonymous_messaging'),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_toggle_anonymous_messaging_mode,
        Text('toggle-anonymous-messaging-mode'),
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
