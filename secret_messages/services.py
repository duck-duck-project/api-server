from uuid import UUID

from django.db import IntegrityError

from secret_messages.exceptions import SecretMediaAlreadyExistsError
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretMessage
from users.models import Contact

__all__ = (
    'create_secret_message',
    'create_secret_media',
)


def create_secret_message(
        *,
        secret_message_id: UUID,
        text: str,
        sender_id: int,
        recipient_id: int,
) -> SecretMessage:
    """Create secret message.

    Args:
        secret_message_id: ID of the secret message.
        text: Text of the secret message.
        sender_id: Telegram ID of the sender user.
        recipient_id: Telegram ID of the recipient user.

    Returns:
        Created SecretMessage object.
    """
    return SecretMessage.objects.create(
        id=secret_message_id,
        text=text,
        sender_id=sender_id,
        recipient_id=recipient_id,
    )


def create_secret_media(
        *,
        file_id: str,
        name: str | None,
        contact: Contact,
        media_type: int,
) -> SecretMedia:
    """Create secret media.

    Args:
        file_id: ID of the file in Telegram.
        name: Name of the file.
        contact: Contact object.
        media_type: Media type.

    Returns:
        Created SecretMedia object.

    Raises:
        SecretMediaAlreadyExistsError: If secret media with the same file_id.
    """
    try:
        return SecretMedia.objects.create(
            file_id=file_id,
            name=name,
            contact=contact,
            media_type=media_type,
        )
    except IntegrityError:
        raise SecretMediaAlreadyExistsError
