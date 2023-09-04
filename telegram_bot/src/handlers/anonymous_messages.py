from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from exceptions import UserHasNoPremiumSubscriptionError
from models import User
from services import determine_media_file_id_and_answer_method
from states import AnonymousMessagingStates
from views import (
    AnonymousMessagingToggledInGroupChatView,
    AnonymousMessagingEnabledView,
    AnonymousMessageSentView,
)
from views import answer_view

__all__ = ('router',)

router = Router(name=__name__)


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
        user: User,
        state: FSMContext,
) -> None:
    if not user.is_premium:
        await message.reply(
            '🌟 Анонимные сообщения только для премиум пользователей'
        )
        return
    await state.set_state(AnonymousMessagingStates.enabled)
    view = AnonymousMessagingEnabledView()
    await answer_view(message=message, view=view)


router.message.register(
    on_toggle_anonymous_messaging_mode_in_group_chat,
    Command('anonymous_messaging'),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
router.message.register(
    on_toggle_anonymous_messaging_mode,
    F.text.in_({
        '/anonymous_messaging',
        '🔐 Включить анонимные сообщения',
    }),
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
router.message.register(
    on_video_note_or_sticker_for_retranslation,
    or_f(F.video_note, F.sticker),
    F.chat.type == ChatType.PRIVATE,
    StateFilter(AnonymousMessagingStates.enabled),
)
router.message.register(
    on_media_for_retranslation,
    or_f(
        F.photo,
        F.audio,
        F.voice,
        F.animation,
        F.document,
        F.video,
    ),
    F.chat.type == ChatType.PRIVATE,
    StateFilter(AnonymousMessagingStates.enabled),
)
router.message.register(
    on_message_for_retranslation,
    F.text,
    F.chat.type == ChatType.PRIVATE,
    StateFilter(AnonymousMessagingStates.enabled),
)
