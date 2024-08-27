from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from secret_messages.exceptions import SecretMediaMessageNotFoundError
from secret_messages.models import SecretMedia
from secret_messages.selectors.text import UserPartialDTO, map_user_to_partial_dto
from users.selectors.contacts import ThemeDTO

__all__ = (
    'get_secret_media_message',
    'SecretMediaMessageDTO',
)


@dataclass(frozen=True, slots=True)
class SecretMediaMessageDTO:
    id: UUID
    sender: UserPartialDTO
    recipient: UserPartialDTO
    theme: ThemeDTO | None
    file_id: str
    caption: str | None
    media_type: int
    created_at: datetime


def get_secret_media_message(
        secret_media_message_id: UUID,
) -> SecretMediaMessageDTO:
    """Get secret media by id.

    Args:
        secret_media_message_id: ID of SecretMedia object.

    Returns:
        SecretMedia object.

    Raises:
        SecretMediaMessageNotFoundError: If SecretMedia object does not exist.
    """
    try:
        secret_media = (
            SecretMedia.objects
            .select_related(
                'contact',
                'contact__of_user',
                'contact__to_user',
                'contact__theme',
                'contact__of_user__theme',
            )
            .get(id=secret_media_message_id)
        )
    except SecretMedia.DoesNotExist:
        raise SecretMediaMessageNotFoundError

    theme = secret_media.contact.theme or secret_media.contact.of_user.theme

    return SecretMediaMessageDTO(
        id=secret_media.id,
        sender=map_user_to_partial_dto(secret_media.contact.of_user),
        recipient=map_user_to_partial_dto(secret_media.contact.to_user),
        theme=theme,
        file_id=secret_media.file_id,
        caption=secret_media.caption,
        media_type=secret_media.media_type,
        created_at=secret_media.created_at,
    )
