from django.db.models import QuerySet

from users.exceptions import ContactDoesNotExistError
from users.models import Contact, User

__all__ = (
    'get_not_deleted_contact_by_id',
    'get_not_deleted_contacts_by_user_id',
)


CONTACTS_SORTING_STRATEGY_TO_FIELD_NAME = {
    User.ContactsSortingStrategy.CREATION_TIME.value: 'created_at',
    User.ContactsSortingStrategy.PUBLIC_NAME.value: 'public_name',
    User.ContactsSortingStrategy.PRIVATE_NAME.value: 'private_name',
}


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
                'of_user__theme',
                'to_user__theme',
            )
            .get(id=contact_id, is_deleted=False)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError


def get_not_deleted_contacts_by_user_id(user: User) -> QuerySet[Contact]:
    """Retrieve contacts of user that are not marked as deleted.

    Args:
        user: User object.

    Returns:
        QuerySet of contacts.
    """

    contacts = (
        Contact.objects
        .select_related(
            'of_user',
            'to_user',
            'of_user__theme',
            'to_user__theme',
        )
        .filter(of_user=user, is_deleted=False)
    )

    sorting_field_name = CONTACTS_SORTING_STRATEGY_TO_FIELD_NAME[
        user.contacts_sorting_strategy
    ]
    if user.is_contacts_sorting_reversed:
        sorting_field_name = f'-{sorting_field_name}'

    return contacts.order_by(sorting_field_name)
