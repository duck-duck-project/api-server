from secret_messages.models.secret_medias import SecretMedia
from secret_messages.selectors.media import SecretMediaMessageDTO
from secret_messages.selectors.text import map_user_to_partial_dto
from users.selectors.contacts import UserContactDTO

__all__ = ('create_secret_media_message',)


def create_secret_media_message(
        *,
        file_id: str,
        caption: str | None,
        user_contact: UserContactDTO,
        media_type: int,
) -> SecretMediaMessageDTO:
    """Create secret media.

    Args:
        file_id: ID of the file in Telegram.
        caption: Caption of the file.
        user_contact: User's contact object.
        media_type: Media type.

    Returns:
        Created SecretMedia object.

    Raises:
        SecretMediaAlreadyExistsError: If secret media with the same file_id.
    """
    secret_media = SecretMedia.objects.create(
        file_id=file_id,
        caption=caption,
        contact_id=user_contact.contact.id,
        media_type=media_type,
    )

    theme = user_contact.contact.theme or user_contact.user.theme

    return SecretMediaMessageDTO(
        id=secret_media.id,
        sender=map_user_to_partial_dto(user_contact.user),
        recipient=map_user_to_partial_dto(user_contact.contact.user),
        theme=theme,
        file_id=secret_media.file_id,
        caption=secret_media.caption,
        media_type=secret_media.media_type,
        created_at=secret_media.created_at,
    )
