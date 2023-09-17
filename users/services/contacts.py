from users.models import User, Contact

__all__ = (
    'create_contact',
    'update_contact',
    'delete_contact_by_id',
)


def create_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
) -> tuple[Contact, bool]:
    """Create contact. If soft deleted, mark it as not deleted.

    Keyword Args:
        of_user: user that owns contact.
        to_user: user that is contact.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.

    Returns:
        Tuple of contact and whether it was created or not.
    """
    return Contact.objects.update_or_create(
        of_user=of_user,
        to_user=to_user,
        defaults={
            'private_name': private_name,
            'public_name': public_name,
            'is_deleted': False,
        },
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
        .filter(id=contact_id)
        .update(is_deleted=True)
    )
    return bool(deleted_count)
