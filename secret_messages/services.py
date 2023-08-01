from uuid import UUID

from django.db import IntegrityError

from secret_messages.exceptions import (
    ContactAlreadyExistsError,
    ContactDoesNotExistError,
)
from secret_messages.models import Contact, SecretMessage
from users.models import User

__all__ = (
    'upsert_contact',
    'update_contact',
    'create_secret_message',
)


def upsert_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
) -> tuple[Contact, bool]:
    try:
        return Contact.objects.update_or_create(
            of_user=of_user,
            to_user=to_user,
            defaults={
                'private_name': private_name,
                'public_name': public_name,
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
) -> None:
    contacts_to_update = Contact.objects.filter(id=contact_id)
    updated_rows_count = contacts_to_update.update(
        private_name=private_name,
        public_name=public_name,
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
