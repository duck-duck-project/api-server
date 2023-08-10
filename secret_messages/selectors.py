from uuid import UUID

from django.db.models import QuerySet

from secret_messages.exceptions import SecretMessageDoesNotExistError
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_message_templates import (
    SecretMessageDescriptionTemplate,
    SecretMessageButtonTemplate,
)
from secret_messages.models.secret_messages import SecretMessage

__all__ = (
    'get_secret_message_by_id',
    'get_secret_medias_created_by_user_id',
    'get_secret_media_by_id',
    'get_secret_message_button_templates',
    'get_secret_message_description_templates',
)


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


def get_secret_medias_created_by_user_id(
        user_id: int,
        media_type: int | None = None,
) -> QuerySet[SecretMedia]:
    """Get secret media created by user_id.

    Args:
        user_id: User Telegram ID.
        media_type: Type of media. If None, then return all media.

    Returns:
        QuerySet of SecretMedia objects.
    """
    secret_medias = (
        SecretMedia.objects
        .select_related('contact', 'contact__of_user', 'contact__to_user')
        .filter(contact__of_user_id=user_id)
    )
    if media_type is not None:
        secret_medias = secret_medias.filter(media_type=media_type)
    return secret_medias


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


def get_secret_message_description_templates() -> (
        QuerySet[SecretMessageDescriptionTemplate]
):
    """Get all secret message description templates."""
    return SecretMessageDescriptionTemplate.objects.all()


def get_secret_message_button_templates() -> (
        QuerySet[SecretMessageButtonTemplate]
):
    """Get all secret message button templates."""
    return SecretMessageButtonTemplate.objects.all()
