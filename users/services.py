from django.db import IntegrityError

from users.exceptions import ContactAlreadyExistsError, ContactDoesNotExistError
from users.models import User, Contact

__all__ = (
    'upsert_user',
    'upsert_contact',
    'update_contact',
)


def upsert_user(
        *,
        user_id: int,
        fullname: str,
        username: str | None,
        can_be_added_to_contacts: bool,
) -> tuple[User, bool]:
    """Create user or update user if already exists.

    Keyword Args:
        user_id: Telegram ID of user.
        fullname: name of user.
        username: username of user.
        can_be_added_to_contacts: whether user can be added to contacts.

    Returns:
        User instance and boolean that indicates
        whether user has been created or not.
    """
    return User.objects.update_or_create(
        id=user_id,
        defaults={
            'fullname': fullname,
            'username': username,
            'can_be_added_to_contacts': can_be_added_to_contacts,
        },
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
