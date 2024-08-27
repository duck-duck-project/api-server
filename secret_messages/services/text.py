from uuid import UUID

from django.db import IntegrityError
from django.db.models.functions import Now

from secret_messages.exceptions import SecretTextMessageIdConflictError
from secret_messages.models.secret_messages import SecretTextMessage
from secret_messages.selectors.text import (
    SecretTextMessageDTO,
    map_user_to_partial_dto, map_user_to_with_can_receive_notifications_dto,
)
from users.selectors.contacts import UserContactDTO

__all__ = (
    'create_secret_text_message',
    'delete_secret_text_message',
    'mark_secret_message_as_seen',
)


def create_secret_text_message(
        *,
        secret_text_message_id: UUID,
        text: str,
        user_contact: UserContactDTO,
) -> SecretTextMessageDTO:
    """Create secret message.

    Args:
        secret_text_message_id: ID of the secret message.
        text: Text of the secret message.
        user_contact: UserContactDTO object.

    Returns:
        Created SecretMessage object.
    """
    try:
        secret_message = SecretTextMessage.objects.create(
            id=secret_text_message_id,
            text=text,
            contact_id=user_contact.contact.id,
        )
    except IntegrityError as error:
        if (
                'duplicate key value violates unique constraint'
                ' "secret_messages_secrettextmessage_pkey"'
        ) in str(error):
            raise SecretTextMessageIdConflictError
        raise

    theme = user_contact.contact.theme or user_contact.user.theme

    return SecretTextMessageDTO(
        id=secret_message.id,
        text=secret_message.text,
        theme=theme,
        sender=map_user_to_partial_dto(user_contact.user),
        recipient=map_user_to_with_can_receive_notifications_dto(
            user=user_contact.contact.user
        ),
        deleted_at=secret_message.deleted_at,
        seen_at=secret_message.seen_at,
        created_at=secret_message.created_at,
    )


def mark_secret_message_as_seen(
        secret_message_id: UUID,
) -> bool:
    """Mark secret message as seen.

    Args:
        secret_message_id: ID of the secret message.

    Returns:
        True if the secret message was marked as seen, False otherwise.
    """
    updated_count = (
        SecretTextMessage.objects
        .filter(id=secret_message_id, deleted_at__isnull=True)
        .update(seen_at=Now())
    )
    return bool(updated_count)


def delete_secret_text_message(
        secret_text_message_id: UUID,
) -> bool:
    """Soft delete secret message.

    Args:
        secret_text_message_id: ID of the secret message.

    Returns:
        True if the secret message was marked as deleted, False otherwise.
    """
    updated_count = (
        SecretTextMessage.objects
        .filter(id=secret_text_message_id)
        .update(deleted_at=Now())
    )
    return bool(updated_count)
