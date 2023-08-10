from uuid import UUID

from django.db import IntegrityError

from secret_messages.exceptions import (
    ContactAlreadyExistsError,
    ContactDoesNotExistError,
    SecretMediaAlreadyExistsError,
)
from secret_messages.models.contacts import Contact
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretMessage
from users.models import User

__all__ = (
    'upsert_contact',
    'update_contact',
    'create_secret_message',
    'create_secret_media',
)


def upsert_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
        is_hidden: bool,
) -> tuple[Contact, bool]:
    try:
        return Contact.objects.update_or_create(
            of_user=of_user,
            to_user=to_user,
            defaults={
                'private_name': private_name,
                'public_name': public_name,
                'is_hidden': is_hidden,
            },
        )
    except IntegrityError as error:
        if 'UNIQUE constraint failed' in str(error):
            raise ContactAlreadyExistsError
        raise


def update_contact(
        *,
        contact_id: int,
        private_name: str,
        public_name: str,
        is_hidden: bool,
) -> None:
    contacts_to_update = Contact.objects.filter(id=contact_id)
    updated_rows_count = contacts_to_update.update(
        private_name=private_name,
        public_name=public_name,
        is_hidden=is_hidden,
    )
    if not updated_rows_count:
        raise ContactDoesNotExistError(contact_id=contact_id)


def create_secret_message(
        *,
        secret_message_id: UUID,
        text: str,
) -> SecretMessage:
    return SecretMessage.objects.create(
        id=secret_message_id,
        text=text,
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
    except IntegrityError as error:
        raise SecretMediaAlreadyExistsError
