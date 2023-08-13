from collections.abc import Coroutine, Callable
from typing import Any
from uuid import UUID

from aiogram.types import Message

from anonymous_messaging.services import HasFileID
from secret_messaging.exceptions import (
    InvalidSecretMediaDeeplinkError,
    UserDoesNotExistError
)
from secret_messaging.models import Contact, SecretMediaType, User

__all__ = (
    'can_see_secret',
    'extract_secret_media_id',
    'determine_media_file',
    'get_message_method_by_media_type',
    'can_create_new_contact',
)

from secret_messaging.repositories import UserRepository


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
