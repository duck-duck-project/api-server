from django.db.models import QuerySet

from users.exceptions import ContactDoesNotExistError
from users.models import Contact

__all__ = (
    'get_contact_by_user_ids',
    'get_contact_by_id',
    'get_contacts_by_user_id',
)


def get_contact_by_user_ids(
        *,
        of_user_id: int,
        to_user_id: int,
) -> Contact:
    """Retrieve contact instance by user IDs.

    Args:
        of_user_id: ID of user who adds contact.
        to_user_id: ID of user who is added to contacts.

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
                'of_user__secret_message_theme',
                'to_user__secret_message_theme',
            )
            .get(of_user_id=of_user_id, to_user_id=to_user_id)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError


def get_contact_by_id(contact_id: int) -> Contact:
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
                'of_user__secret_message_theme',
                'to_user__secret_message_theme',
            )
            .get(id=contact_id)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError


def get_contacts_by_user_id(user_id: int) -> QuerySet[Contact]:
    """Retrieve contacts of user.

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
            'of_user__secret_message_theme',
            'to_user__secret_message_theme',
        )
        .filter(of_user_id=user_id)
    )
