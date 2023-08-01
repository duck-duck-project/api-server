from uuid import UUID

from django.db.models import QuerySet

from secret_messages.exceptions import (
    ContactDoesNotExistError,
    SecretMessageDoesNotExistError,
)
from secret_messages.models import Contact, SecretMessage

__all__ = (
    'get_contact_by_id',
    'get_contacts_by_user_id',
    'get_secret_message_by_id',
)


def get_contact_by_id(contact_id: int) -> Contact:
    try:
        return (
            Contact.objects
            .select_related('of_user', 'to_user')
            .get(id=contact_id)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError(contact_id=contact_id)


def get_contacts_by_user_id(user_id: int) -> QuerySet[Contact]:
    return (
        Contact.objects
        .select_related('of_user', 'to_user')
        .filter(of_user_id=user_id)
    )


def get_secret_message_by_id(secret_message_id: UUID) -> SecretMessage:
    try:
        return SecretMessage.objects.get(id=secret_message_id)
    except SecretMessage.DoesNotExist:
        raise SecretMessageDoesNotExistError(
            secret_message_id=secret_message_id,
        )
