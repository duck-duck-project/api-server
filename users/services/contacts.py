from dataclasses import dataclass
from datetime import datetime

from django.db import transaction

from users.exceptions import ContactAlreadyExistsError
from users.models import Contact, User

__all__ = (
    'create_contact',
    'update_contact',
    'delete_contact_by_id',
)


@dataclass(frozen=True, slots=True)
class UserPartialDTO:
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class ContactDTO:
    id: int
    user: UserPartialDTO
    private_name: str
    public_name: str
    is_hidden: bool
    theme: None
    created_at: datetime


@transaction.atomic
def create_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
) -> ContactDTO:
    """Create contact. If soft deleted, mark it as not deleted.
    Withdraw funds from user for contact creation.

    Keyword Args:
        of_user: user that owns contact.
        to_user: user that is contact.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.

    Returns:
        Contact instance.

    Raises:
        ContactAlreadyExistsError: if contact already exists.
    """
    try:
        contact = Contact.objects.get(of_user=of_user, to_user=to_user)
    except Contact.DoesNotExist:
        contact = Contact.objects.create(
            of_user=of_user,
            to_user=to_user,
            private_name=private_name,
            public_name=public_name,
        )
    else:
        if contact.is_deleted:
            contact.is_deleted = False
            contact.save()
        else:
            raise ContactAlreadyExistsError

    return ContactDTO(
        id=contact.id,
        user=UserPartialDTO(
            id=to_user.id,
            fullname=to_user.fullname,
            username=to_user.username,
        ),
        private_name=contact.private_name,
        public_name=contact.public_name,
        is_hidden=contact.is_hidden,
        theme=contact.theme,
        created_at=contact.created_at,
    )


def update_contact(
        *,
        contact_id: int,
        private_name: str,
        public_name: str,
        is_hidden: bool,
) -> bool:
    """Update contact.

    Keyword Args:
        contact_id: id of contact to update.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.
        is_hidden: whether contact is hidden from user.
    """
    updated_count = Contact.objects.filter(id=contact_id).update(
        private_name=private_name,
        public_name=public_name,
        is_hidden=is_hidden,
    )
    return bool(updated_count)


def delete_contact_by_id(contact_id: int) -> bool:
    """Soft delete contact by id.

    Keyword Args:
        contact_id: id of contact to delete.

    Returns:
        True if contact was marked as deleted, False otherwise.
    """
    deleted_count = (
        Contact
        .objects
        .filter(id=contact_id, is_deleted=False)
        .update(is_deleted=True)
    )
    return bool(deleted_count)
