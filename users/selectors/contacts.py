from django.db.models import QuerySet

from users.exceptions import ContactDoesNotExistError
from users.models import Contact

__all__ = (
    'get_not_deleted_contact_by_id',
    'get_not_deleted_contacts_by_user_id',
)


def get_not_deleted_contact_by_id(contact_id: int) -> Contact:
    """Retrieve contact instance by ID.

    Args:
        contact_id: ID of contact.

    Returns:
        Contact instance if exists.

    Raises:
        ContactDoesNotExistError: If contact does not exist.
    """
    try:
        return (
            Contact.objects
            .select_related(
                'of_user',
                'to_user',
                'of_user__theme_id',
                'to_user__theme_id',
            )
            .get(id=contact_id, is_deleted=False)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError


def get_not_deleted_contacts_by_user_id(user_id: int) -> QuerySet[Contact]:
    """Retrieve contacts of user that are not marked as deleted.

    Args:
        user_id: ID of user.

    Returns:
        QuerySet of contacts.
    """
    return (
        Contact.objects
        .select_related(
            'of_user',
            'to_user',
            'of_user__theme',
            'to_user__theme',
        )
        .filter(of_user_id=user_id, is_deleted=False)
    )
