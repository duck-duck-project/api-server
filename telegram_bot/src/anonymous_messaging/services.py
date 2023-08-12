from collections.abc import Callable, Awaitable
from typing import Protocol, TypeAlias

from aiogram.types import Message

__all__ = (
    'is_anonymous_messaging_enabled',
    'HasVideoPhotoAnimationVoiceAudioDocument',
    'HasFileID',
    'HasSendVideoPhotoAnimationVoiceAudioDocumentMethod',
    'determine_media_file_id_and_answer_method',
    'ReturnsMessage',
)

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
