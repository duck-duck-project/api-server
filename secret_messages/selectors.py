from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from django.db.models import Q

from secret_messages.exceptions import SecretMessageDoesNotExistError
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretMessage
from users.models import Contact

__all__ = (
    'get_secret_message_by_id',
    'get_secret_media_by_id',
    'ContactSecretMessage',
    'ContactPartial',
    'ContactSecretMessages',
    'get_contact_secret_messages',
)


@dataclass(frozen=True, slots=True)
class UserPartial:
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class ContactSecretMessage:
    id: UUID
    text: str
    sender_id: int
    recipient_id: int
    created_at: datetime
    seen_at: datetime | None


@dataclass(frozen=True, slots=True)
class ContactPartial:
    id: int
    of_user: UserPartial
    to_user: UserPartial


@dataclass(frozen=True, slots=True)
class ContactSecretMessages:
    contact: ContactPartial
    secret_messages: list[ContactSecretMessage]


def get_secret_message_by_id(secret_message_id: UUID) -> SecretMessage:
    """Get secret message by ID.

    Args:
        secret_message_id: ID of the secret message.

    Returns:
        SecretMessage object.

    Raises:
        SecretMessageDoesNotExistError: If secret message with the given ID
    """
    try:
        return SecretMessage.objects.get(id=secret_message_id)
    except SecretMessage.DoesNotExist:
        raise SecretMessageDoesNotExistError(
            secret_message_id=secret_message_id,
        )


def get_secret_media_by_id(secret_media_id: UUID) -> SecretMedia:
    """Get secret media by id.

    Args:
        secret_media_id: ID of SecretMedia object.

    Returns:
        SecretMedia object.

    Raises:
        SecretMessageDoesNotExistError: If SecretMedia object does not exist.
    """
    try:
        return (
            SecretMedia.objects
            .select_related('contact', 'contact__of_user',
                            'contact__to_user')
            .get(id=secret_media_id)
        )
    except SecretMedia.DoesNotExist:
        raise SecretMessageDoesNotExistError(
            secret_message_id=secret_media_id,
        )


def get_contact_secret_messages(contact: Contact) -> ContactSecretMessages:
    contact_secret_messages = (
        SecretMessage.objects
        .filter(
            Q(
                recipient_id=contact.to_user_id,
                sender_id=contact.of_user_id,
            ) | Q(
                recipient_id=contact.of_user_id,
                sender_id=contact.to_user_id,
            ),
            deleted_at__isnull=True,
        )
        .order_by('created_at')
    )
    secret_messages = (
        contact_secret_messages
        .values(
            'id',
            'text',
            'sender_id',
            'recipient_id',
            'created_at',
            'seen_at',
        )
    )
    contact_secret_messages = [
        ContactSecretMessage(
            id=secret_message['id'],
            text=secret_message['text'],
            sender_id=secret_message['sender_id'],
            recipient_id=secret_message['recipient_id'],
            created_at=secret_message['created_at'],
            seen_at=secret_message['seen_at'],
        )
        for secret_message in secret_messages
    ]
    contact_partial = ContactPartial(
        id=contact.id,
        of_user=UserPartial(
            id=contact.of_user.id,
            fullname=contact.of_user.fullname,
            username=contact.of_user.username,
        ),
        to_user=UserPartial(
            id=contact.to_user.id,
            fullname=contact.to_user.fullname,
            username=contact.to_user.username,
        ),
    )

    return ContactSecretMessages(
        contact=contact_partial,
        secret_messages=contact_secret_messages,
    )
