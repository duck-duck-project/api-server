import contextlib
from collections.abc import Coroutine, Callable, Awaitable, Iterable
from typing import Protocol, TypeAlias, TypeVar, Any
from uuid import UUID

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.exceptions import (
    TelegramAPIError, BotBlocked,
    CantInitiateConversation, ChatNotFound
)

from exceptions import InvalidSecretMediaDeeplinkError, UserDoesNotExistError
from models import User
from models.contacts import Contact
from models.secret_media_types import SecretMediaType
from repositories import UserRepository
from views.base import View
from views import SecretMessageNotificationView

__all__ = (
    'is_anonymous_messaging_enabled',
    'HasVideoPhotoAnimationVoiceAudioDocument',
    'HasFileID',
    'HasSendVideoPhotoAnimationVoiceAudioDocumentMethod',
    'determine_media_file_id_and_answer_method',
    'ReturnsMessage',
    'can_see_secret',
    'extract_secret_media_id',
    'determine_media_file',
    'get_message_method_by_media_type',
    'can_create_new_contact',
    'get_or_create_user',
    'filter_not_hidden',
    'send_view_to_user',
)


class HasIsHidden(Protocol):
    is_hidden: bool


HasIsHiddenT = TypeVar('HasIsHiddenT', bound=HasIsHidden)
ReturnsMessage: TypeAlias = Callable[..., Awaitable[Message]]


class HasSendVideoPhotoAnimationVoiceAudioDocumentMethod(Protocol):

    async def send_photo(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...

    async def send_video(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...

    async def send_animation(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...

    async def send_voice(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...

    async def send_audio(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...

    async def send_document(
            self,
            chat_id: int | str,
            file_id: str,
            caption: str | None,
    ) -> Message: ...


class HasFileID(Protocol):
    file_id: str


class HasVideoPhotoAnimationVoiceAudioDocument(Protocol):
    photo: list[HasFileID]
    video: HasFileID | None
    animation: HasFileID | None
    voice: HasFileID | None
    audio: HasFileID | None
    document: HasFileID | None


def is_anonymous_messaging_enabled(state_name: str) -> bool:
    # rename it if state declaration will be changed
    # in anonymous_messaging.states.py file
    return state_name == 'AnonymousMessagingStates:enabled'


def determine_media_file_id_and_answer_method(
        bot: HasSendVideoPhotoAnimationVoiceAudioDocumentMethod,
        message: HasVideoPhotoAnimationVoiceAudioDocument,
) -> tuple[HasFileID, ReturnsMessage]:
    """Determine media type and answer method."""

    methods_and_medias = [
        (bot.send_video, message.video),
        (bot.send_animation, message.animation),
        (bot.send_voice, message.voice),
        (bot.send_audio, message.audio),
        (bot.send_document, message.document),
    ]
    if message.photo:
        methods_and_medias.append((bot.send_photo, message.photo[-1]))

    for method, media in methods_and_medias:
        if media is not None:
            return media.file_id, method
    raise ValueError('Unsupported media type')


def can_see_secret(
        *,
        user_id: int,
        contact: Contact,
) -> bool:
    return user_id in (
        contact.of_user.id,
        contact.to_user.id,
    )


def extract_secret_media_id(deep_link: str) -> UUID:
    try:
        return UUID(deep_link.split('-')[-1])
    except (ValueError, IndexError):
        raise InvalidSecretMediaDeeplinkError


def determine_media_file(message: Message) -> tuple[str, SecretMediaType]:
    medias_and_media_types: list[tuple[HasFileID, SecretMediaType]] = [
        (message.voice, SecretMediaType.VOICE),
        (message.video, SecretMediaType.VIDEO),
        (message.audio, SecretMediaType.AUDIO),
        (message.animation, SecretMediaType.ANIMATION),
        (message.document, SecretMediaType.DOCUMENT),
        (message.video_note, SecretMediaType.VIDEO_NOTE),
        (message.sticker, SecretMediaType.STICKER),
    ]
    if message.photo:
        medias_and_media_types.append(
            (message.photo[-1], SecretMediaType.PHOTO)
        )
    for media, media_type in medias_and_media_types:
        if media is not None:
            return media.file_id, media_type
    raise ValueError('Unsupported media type')


def get_message_method_by_media_type(
        *,
        message: Message,
        media_type: SecretMediaType,
) -> Callable[..., Coroutine[Any, Any, Message]]:
    media_type_to_method = {
        SecretMediaType.PHOTO: message.answer_photo,
        SecretMediaType.VOICE: message.answer_voice,
        SecretMediaType.ANIMATION: message.answer_animation,
        SecretMediaType.VIDEO: message.answer_video,
        SecretMediaType.VIDEO_NOTE: message.answer_video_note,
        SecretMediaType.STICKER: message.answer_sticker,
        SecretMediaType.DOCUMENT: message.answer_document,
        SecretMediaType.AUDIO: message.answer_audio,
    }
    try:
        return media_type_to_method[media_type]
    except KeyError:
        raise ValueError('Unsupported media type')


async def get_or_create_user(
        *,
        user_id: int,
        fullname: str,
        username: str | None,
        user_repository: UserRepository,
) -> tuple[User, bool]:
    try:
        return await user_repository.get_by_id(user_id=user_id), False
    except UserDoesNotExistError:
        return await user_repository.create(
            user_id=user_id,
            fullname=fullname,
            username=username,
        ), True


def can_create_new_contact(
        *,
        contacts_count: int,
        is_premium: bool,
) -> bool:
    return contacts_count < 5 or is_premium


def filter_not_hidden(items: Iterable[HasIsHiddenT]) -> list[HasIsHiddenT]:
    return [item for item in items if not item.is_hidden]


async def send_view_to_user(
        *,
        bot: Bot,
        view: View,
        to_chat_id: int,
        from_chat_id: int,
) -> None:
    try:
        await bot.send_message(
            to_chat_id,
            text=view.get_text(),
            reply_markup=view.get_reply_markup(),
        )
    except BotBlocked:
        with contextlib.suppress(TelegramAPIError):
            await bot.send_message(
                chat_id=from_chat_id,
                text=(
                    '❌ Не удалось отправить сообщение.'
                    ' Пользователь заблокировал бота'
                ),
            )
    except CantInitiateConversation:
        with contextlib.suppress(TelegramAPIError):
            await bot.send_message(
                chat_id=from_chat_id,
                text=(
                    '❌ Не удалось отправить сообщение.'
                    ' Пользователь пока не начинал диалог с ботом'
                ),
            )
    except ChatNotFound:
        with contextlib.suppress(TelegramAPIError):
            await bot.send_message(
                chat_id=from_chat_id,
                text=(
                    '❌ Не удалось отправить сообщение.'
                    ' Пользователь не существует'
                ),
            )
    except TelegramAPIError as error:
        with contextlib.suppress(TelegramAPIError):
            await bot.send_message(
                chat_id=from_chat_id,
                text='❌ Не удалось отправить сообщение.',
            )
    else:
        await bot.send_message(
            chat_id=from_chat_id,
            text='✅ Секретное сообщение отправлено',
            disable_notification=True,
        )
